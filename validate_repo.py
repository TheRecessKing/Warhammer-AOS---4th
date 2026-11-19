import glob
import json
import os
import sys

ROOT_DIR = "."
GS_FILE = "Warhammer Age of Sigmar.json"
SKIP_FILES = {GS_FILE, "index.json", "manifest.json"}


def walk(node, f_label, ids, refs, profiles, path="root"):
  """Recursively walks JSON structures to collect IDs, references, and profiles."""
  if isinstance(node, dict):
    if "id" in node and node["id"]:
      ids.setdefault(node["id"], []).append(
          f"{path} ({node.get('name', '<unnamed>')})"
      )
    for rk in ("targetId", "childId", "typeId"):
      if rk in node and node[rk] is not None:
        refs.append(
            (f_label, f"{path}.{rk}", node.get("name", "<unnamed>"), node[rk])
        )
    if "typeId" in node and "characteristics" in node:
      profiles.append((f_label, path, node))
    for k, v in node.items():
      if isinstance(v, (dict, list)):
        walk(v, f_label, ids, refs, profiles, f"{path}.{k}")
  elif isinstance(node, list):
    for i, item in enumerate(node):
      walk(item, f_label, ids, refs, profiles, f"{path}[{i}]")


def main():
  if not os.path.exists(GS_FILE):
    print(f"ERROR: Missing '{GS_FILE}' in root folder.")
    return 1

  with open(GS_FILE, "r", encoding="utf-8") as f:
    gs = json.load(f)["gameSystem"]

  gs_id = gs["id"]
  gs_ids, gs_refs, all_profiles = {}, [], []
  walk(gs, GS_FILE, gs_ids, gs_refs, all_profiles, "gameSystem")

  expected_chars = {
      pt["id"]: {ct["id"]: ct["name"] for ct in pt.get("characteristicTypes", [])}
      for pt in gs.get("profileTypes", [])
  }

  errors = []
  global_owners = {uid: [GS_FILE] for uid in gs_ids}
  for uid, locs in gs_ids.items():
    if len(locs) > 1:
      errors.append(f"[{GS_FILE}] Duplicate ID '{uid}': {locs}")

  cat_files = sorted(
      p
      for p in glob.glob(os.path.join(ROOT_DIR, "*.json"))
      if os.path.basename(p) not in SKIP_FILES
  )

  for cpath in cat_files:
    cname = os.path.basename(cpath)
    with open(cpath, "r", encoding="utf-8") as f:
      cat = json.load(f)["catalogue"]
    if cat.get("gameSystemId") != gs_id:
      errors.append(
          f"[{cname}] gameSystemId '{cat.get('gameSystemId')}' does not match"
          f" '{gs_id}'."
      )
    c_ids, c_refs, c_profs = {}, [], []
    walk(cat, cname, c_ids, c_refs, c_profs, "catalogue")
    for uid, locs in c_ids.items():
      if len(locs) > 1:
        errors.append(f"[{cname}] Duplicate ID '{uid}': {locs}")
      global_owners.setdefault(uid, []).append(cname)
    pool = set(gs_ids.keys()) | set(c_ids.keys())
    for fl, rp, own, tid in c_refs:
      if tid not in pool:
        errors.append(f"[{fl}] Broken ref '{tid}' on '{own}' ({rp})")
    all_profiles.extend(c_profs)

  for fl, rp, own, tid in gs_refs:
    if tid not in gs_ids:
      errors.append(f"[{fl}] Broken GS ref '{tid}' on '{own}' ({rp})")

  for uid, owners in global_owners.items():
    if len(owners) > 1:
      errors.append(f"[CROSS-FILE] Duplicate ID '{uid}' in {owners}")

  for fl, pp, prof in all_profiles:
    req = expected_chars.get(prof.get("typeId"), {})
    present = {ch.get("typeId"): ch for ch in prof.get("characteristics", [])}
    for cid, cname_ch in req.items():
      if cid not in present or not str(present[cid].get("$text", "")).strip():
        errors.append(
            f"[{fl}] Profile '{prof.get('name')}' missing/empty '{cname_ch}'"
            f" ({pp})"
        )

  if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for e in errors:
      print(" ", e)
    return 1

  print(
      f"PASSED: {GS_FILE} + {len(cat_files)} root catalogues valid"
      f" ({len(all_profiles)} profiles)."
  )
  return 0


if __name__ == "__main__":
  sys.exit(main())