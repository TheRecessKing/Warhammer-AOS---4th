from datetime import datetime, timezone
import glob
import hashlib
import json
import os

ROOT_DIR = "."
GS_FILE = "Warhammer Age of Sigmar.json"
REPO_SLUG = "YOUR_GITHUB_USERNAME/aos-4th-newrecruit"
BRANCH = "main"


def sha256_file(path: str) -> str:
  h = hashlib.sha256()
  with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
      h.update(chunk)
  return h.hexdigest()


def main():
  if not os.path.exists(GS_FILE):
    raise FileNotFoundError(f"Missing '{GS_FILE}' in root folder.")

  with open(GS_FILE, "r", encoding="utf-8") as f:
    gs = json.load(f)["gameSystem"]

  gs_record = {
      "file": GS_FILE,
      "raw_url": (
          f"https://raw.githubusercontent.com/{REPO_SLUG}/{BRANCH}/{GS_FILE}"
      ),
      "size_bytes": os.stat(GS_FILE).st_size,
      "sha256": sha256_file(GS_FILE),
      "kind": "gameSystem",
      "id": gs["id"],
      "name": gs["name"],
      "revision": gs.get("revision", 1),
  }

  cat_records = []
  skip = {GS_FILE, "index.json", "manifest.json"}
  for p in sorted(glob.glob(os.path.join(ROOT_DIR, "*.json"))):
    fn = os.path.basename(p)
    if fn in skip:
      continue
    with open(p, "r", encoding="utf-8") as f:
      cat = json.load(f)["catalogue"]
    cat_records.append({
        "file": fn,
        "raw_url": f"https://raw.githubusercontent.com/{REPO_SLUG}/{BRANCH}/{fn}",
        "size_bytes": os.stat(p).st_size,
        "sha256": sha256_file(p),
        "kind": "catalogue",
        "id": cat["id"],
        "name": cat["name"],
        "revision": cat.get("revision", 1),
        "gameSystemId": cat.get("gameSystemId"),
    })

  manifest = {
      "schema_version": "1.0",
      "generated_at": datetime.now(timezone.utc).isoformat(),
      "repository": {"slug": REPO_SLUG, "branch": BRANCH},
      "counts": {
          "game_systems": 1,
          "catalogues": len(cat_records),
          "total_files": 1 + len(cat_records),
      },
      "gameSystems": [gs_record],
      "catalogues": cat_records,
  }

  for out_name in ("index.json", "manifest.json"):
    with open(out_name, "w", encoding="utf-8") as f:
      json.dump(manifest, f, indent=2)

  print(
      f"Generated root index.json and manifest.json ({len(cat_records)}"
      " catalogues)."
  )


if __name__ == "__main__":
  main()