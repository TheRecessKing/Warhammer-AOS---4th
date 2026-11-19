import hashlib
import json
import os

GS_FILE = "Warhammer Age of Sigmar.json"


def nr_id(seed_str: str) -> str:
  h = hashlib.md5(seed_str.encode("utf-8")).hexdigest()[:16]
  return f"{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"


CATALOGUE_EXPANSIONS = {
    "Cities of Sigmar": {
        "traits": [("Fiery Temper", "Add 1 to charge rolls for friendly Cities of Sigmar units wholly within 12 inches.")],
        "artefacts": [("Brazier of Holy Flame", "Return D3 slain models to a friendly Human Infantry unit wholly within 12 inches in your Hero Phase.")],
        "lores": [("Spells of the Collegiate Arcane", "Pha's Protection", 6, "Target friendly Cities of Sigmar unit within 12 inches subtracts 1 from hit rolls for incoming attacks.")],
        "units": [
            {"name": "Freeguild Command Corps", "pts": 160, "move": '5"', "health": 3, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "CITIES OF SIGMAR"], "reinforce": False, "weapons": [("Command Corps Weapons", 3, "3+", "3+", 1, 1, "-", None)], "abilities": [("Dispatch Spies", "Allows a friendly Freeguild Marshal to issue an additional Order each turn.", None)]},
            {"name": "Wildercorps Hunters", "pts": 130, "move": '6"', "health": 2, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "CITIES OF SIGMAR"], "reinforce": False, "weapons": [("Arbalest or Hunter's Bow", 2, "3+", "4+", 1, 1, "-", '18"')], "abilities": [("Outriders of the Wilds", "Can set up in ambush outside friendly territory prior to battle round 1.", "Deployment Phase")]},
        ],
    },
    "Slaves to Darkness": {
        "traits": [("Deathmonger", "Once per battle, fight twice in the Combat Phase.")],
        "artefacts": [("The Conqueror's Crown", "Subtract 5 from control scores of enemy Infantry in combat with this Hero.")],
        "lores": [("Lore of the Damned", "Binding Damnation", 7, "Target visible enemy unit within 12 inches has Strike-last until your next turn.")],
        "units": [
            {"name": "Chaos Knights", "pts": 250, "move": '10"', "health": 4, "save": "3+", "control": 1, "primary": "CAVALRY", "cats": ["CAVALRY", "CHAOS", "SLAVES TO DARKNESS", "WARRIORS OF CHAOS"], "reinforce": True, "weapons": [("Cursed Lance", 3, "3+", "3+", 1, 1, "Anti-charge (+1 Rend), Charge (+1 Damage)", None), ("Steed's Hooves", 2, "5+", "3+", 0, 1, "Companion", None)], "abilities": [("Impaling Charge", "+1 Rend on Cursed Lances when charging.", None)]},
            {"name": "Ogroid Theridons", "pts": 180, "move": '6"', "health": 5, "save": "4+", "control": 2, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "SLAVES TO DARKNESS"], "reinforce": True, "weapons": [("Goroan Great Axe", 4, "4+", "2+", 2, 2, "Anti-INFANTRY (+1 Rend)", None)], "abilities": [("Unleashed Savagery", "+1 melee Damage once per battle.", "Once Per Battle, Any Combat Phase")]},
        ],
    },
}


def load_gs_lookup():
  if not os.path.exists(GS_FILE):
    raise FileNotFoundError(f"Missing '{GS_FILE}' in root folder.")
  with open(GS_FILE, "r", encoding="utf-8") as f:
    gs = json.load(f)["gameSystem"]

  cost_ids = {c["name"]: c["id"] for c in gs.get("costTypes", [])}
  cat_ids = {c["name"]: c["id"] for c in gs.get("categoryEntries", [])}
  pt_map = {}
  for pt in gs.get("profileTypes", []):
    pt_map[pt["name"]] = {
        "id": pt["id"],
        "chars": {ct["name"]: ct["id"] for ct in pt.get("characteristicTypes", [])},
    }
  return gs, cost_ids, cat_ids, pt_map


def make_unit_prof(pt_map, name, move, health, save, control, banish="-"):
  pt = pt_map["Unit"]
  vals = {"Move": move, "Health": health, "Save": save, "Control": control, "Banishment": banish}
  return {
      "name": name,
      "id": nr_id(f"prof-unit-{name}"),
      "hidden": False,
      "typeId": pt["id"],
      "typeName": "Unit",
      "characteristics": [{"name": k, "$text": str(v), "typeId": pt["chars"][k]} for k, v in vals.items()],
  }


def make_weapon_prof(pt_map, parent, name, atk, hit, wnd, rnd, dmg, abil="-", rng=None):
  is_ranged = rng is not None
  pt_name = "Ranged Weapon" if is_ranged else "Melee Weapon"
  pt = pt_map[pt_name]
  vals = {}
  if is_ranged:
    vals["Rng"] = rng
  vals.update({"Atk": atk, "Hit": hit, "Wnd": wnd, "Rnd": rnd, "Dmg": dmg, "Ability": abil})
  return {
      "name": name,
      "id": nr_id(f"prof-w-{parent}-{name}"),
      "hidden": False,
      "typeId": pt["id"],
      "typeName": pt_name,
      "characteristics": [{"name": k, "$text": str(v), "typeId": pt["chars"][k]} for k, v in vals.items()],
  }


def make_abil_prof(pt_map, parent, name, eff, timing=None, declare="-", keywords="-", cost="-", cast_val=None):
  if cast_val is not None:
    pt = pt_map["Ability (Spell / Prayer)"]
    vals = {"Timing": timing or "Your Hero Phase", "Value": cast_val, "Declare": declare, "Effect": eff, "Keywords": keywords}
    return {
        "name": name,
        "id": nr_id(f"prof-abil-{parent}-{name}"),
        "hidden": False,
        "typeId": pt["id"],
        "typeName": "Ability (Spell / Prayer)",
        "characteristics": [{"name": k, "$text": str(v), "typeId": pt["chars"][k]} for k, v in vals.items()],
    }
  if timing:
    pt = pt_map["Ability (Activated)"]
    vals = {"Timing": timing, "Cost": cost, "Declare": declare, "Effect": eff, "Keywords": keywords}
    return {
        "name": name,
        "id": nr_id(f"prof-abil-{parent}-{name}"),
        "hidden": False,
        "typeId": pt["id"],
        "typeName": "Ability (Activated)",
        "characteristics": [{"name": k, "$text": str(v), "typeId": pt["chars"][k]} for k, v in vals.items()],
    }
  pt = pt_map["Ability (Passive)"]
  vals = {"Effect": eff, "Keywords": keywords}
  return {
      "name": name,
      "id": nr_id(f"prof-abil-{parent}-{name}"),
      "hidden": False,
      "typeId": pt["id"],
      "typeName": "Ability (Passive)",
      "characteristics": [{"name": k, "$text": str(v), "typeId": pt["chars"][k]} for k, v in vals.items()],
  }


def main():
  gs, cost_ids, cat_ids, pt_map = load_gs_lookup()
  gs_modified = False

  for exp in CATALOGUE_EXPANSIONS.values():
    for u in exp.get("units", []):
      for c in u["cats"]:
        if c not in cat_ids:
          cid = nr_id(f"cat-{c}")
          cat_ids[c] = cid
          gs["categoryEntries"].append({"id": cid, "name": c, "hidden": False})
          gs_modified = True

  if gs_modified:
    with open(GS_FILE, "w", encoding="utf-8") as gf:
      json.dump({"gameSystem": gs}, gf, indent=2)

  updated_files = 0
  for faction_name, exp in CATALOGUE_EXPANSIONS.items():
    cat_path = f"{faction_name}.json"
    if not os.path.exists(cat_path):
      print(f"Skipping {cat_path} (not found in root folder)")
      continue

    with open(cat_path, "r", encoding="utf-8") as cf:
      doc = json.load(cf)
    cat = doc["catalogue"]
    shared = cat.setdefault("sharedSelectionEntries", [])
    links = cat.setdefault("entryLinks", [])

    for entry in shared:
      if entry.get("name", "").endswith(": Battle Traits, Formations & Lores") and exp.get("lores"):
        groups = entry.setdefault("selectionEntryGroups", [])
        lore_grp = next((g for g in groups if "Lore" in g.get("name", "")), None)
        if lore_grp is None:
          lore_grp = {
              "id": nr_id(f"grp-lore-{faction_name}"),
              "name": "Faction Spell / Prayer Lore",
              "constraints": [{"id": nr_id(f"c-lr-max-{faction_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
              "selectionEntries": [],
          }
          groups.append(lore_grp)
        existing_lores = {se["name"] for se in lore_grp.setdefault("selectionEntries", [])}
        for lr in exp["lores"]:
          l_label = f"{lr[0]}: {lr[1]}"
          if l_label not in existing_lores:
            lore_grp["selectionEntries"].append({
                "id": nr_id(f"lore-{faction_name}-{lr[0]}-{lr[1]}"),
                "name": l_label,
                "type": "upgrade",
                "profiles": [make_abil_prof(pt_map, lr[0], lr[1], lr[3], timing="Your Hero Phase", keywords="Spell / Prayer", cast_val=lr[2])],
            })

    for entry in shared:
      if entry.get("type") == "unit":
        for grp in entry.get("selectionEntryGroups", []):
          if grp.get("name") == "Heroic Traits":
            seen_t = {se["name"] for se in grp.setdefault("selectionEntries", [])}
            for t_name, t_eff in exp.get("traits", []):
              if t_name not in seen_t:
                grp["selectionEntries"].append({
                    "id": nr_id(f"ht-{faction_name}-{entry['name']}-{t_name}"),
                    "name": t_name,
                    "type": "upgrade",
                    "profiles": [make_abil_prof(pt_map, entry["name"], t_name, t_eff)],
                })
          elif grp.get("name") == "Artefacts of Power":
            seen_a = {se["name"] for se in grp.setdefault("selectionEntries", [])}
            for a_name, a_eff in exp.get("artefacts", []):
              if a_name not in seen_a:
                grp["selectionEntries"].append({
                    "id": nr_id(f"art-{faction_name}-{entry['name']}-{a_name}"),
                    "name": a_name,
                    "type": "upgrade",
                    "profiles": [make_abil_prof(pt_map, entry["name"], a_name, a_eff)],
                })

    existing_units = {se["name"] for se in shared}
    added_units = 0
    for u in exp.get("units", []):
      uname = u["name"]
      if uname in existing_units:
        continue
      profs = [make_unit_prof(pt_map, uname, u["move"], u["health"], u["save"], u["control"])]
      for w in u["weapons"]:
        profs.append(make_weapon_prof(pt_map, uname, w[0], w[1], w[2], w[3], w[4], w[5], abil=w[6], rng=w[7]))
      for a in u["abilities"]:
        profs.append(make_abil_prof(pt_map, uname, a[0], a[2], timing=a[1]))

      sub_entries = []
      modifiers = []
      if u.get("reinforce"):
        reinf_id = nr_id(f"reinf-{faction_name}-{uname}")
        sub_entries.append({
            "id": reinf_id,
            "name": "Reinforced",
            "type": "upgrade",
            "constraints": [{"id": nr_id(f"c-reinf-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
        })
        modifiers.append({
            "field": cost_ids["pts"],
            "type": "multiply",
            "value": 2,
            "conditions": [{"childId": reinf_id, "field": "selections", "scope": "self", "type": "atLeast", "value": 1}],
        })
      if u["primary"] == "HERO":
        sub_entries.append({
            "id": nr_id(f"gen-{faction_name}-{uname}"),
            "name": "General",
            "type": "upgrade",
            "constraints": [{"id": nr_id(f"c-gen-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
        })

      uid = nr_id(f"unit-{faction_name}-{uname}")
      shared.append({
          "id": uid,
          "name": uname,
          "type": "unit",
          "hidden": False,
          "import": True,
          "costs": [
              {"name": "pts", "typeId": cost_ids["pts"], "value": u["pts"]},
              {"name": "Glory Points", "typeId": cost_ids["Glory Points"], "value": 0},
              {"name": "Renown", "typeId": cost_ids["Renown"], "value": 0},
          ],
          "categoryLinks": [{
              "id": nr_id(f"cl-{faction_name}-{uname}-{c}"),
              "name": c,
              "hidden": False,
              "primary": c == u["primary"],
              "targetId": cat_ids[c],
          } for c in u["cats"]],
          "profiles": profs,
          "selectionEntries": sub_entries,
          "modifiers": modifiers,
      })
      links.append({
          "id": nr_id(f"el-{faction_name}-{uname}"),
          "name": uname,
          "hidden": False,
          "type": "selectionEntry",
          "targetId": uid,
      })
      added_units += 1

    with open(cat_path, "w", encoding="utf-8") as cf:
      json.dump(doc, cf, indent=2)
    updated_files += 1
    print(f"Updated {cat_path} in-place (+{added_units} warscrolls, traits, artefacts, and lores)")

  print(f"\nDone! Expanded {updated_files} root faction catalogues directly in-place.")


if __name__ == "__main__":
  main()