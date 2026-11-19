import hashlib
import json


def nr_id(seed_str: str) -> str:
  h = hashlib.md5(seed_str.encode("utf-8")).hexdigest()[:16]
  return f"{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"


GS_FILENAME = "Warhammer Age of Sigmar.json"
GS_ID = nr_id("aos4-gamesystem-root-v2")
COST_PTS = nr_id("cost-pts")
COST_GLORY = nr_id("cost-glory")
COST_RENOWN = nr_id("cost-renown")
COST_DESTINY = nr_id("cost-destiny")

PT_UNIT = nr_id("pt-unit")
PT_MELEE = nr_id("pt-melee")
PT_RANGED = nr_id("pt-ranged")
PT_ABIL_ACT = nr_id("pt-ability-activated")
PT_ABIL_PAS = nr_id("pt-ability-passive")
PT_ABIL_SPL = nr_id("pt-ability-spell-prayer")


def char_id(pt_label: str, char_name: str) -> str:
  """Unique characteristicType ID scoped to its parent profileType."""
  return nr_id(f"pt-{pt_label}-char-{char_name}")


CATEGORIES = [
    "Configuration", "Army Composition", "Order of Battle",
    "Manifestation Lore", "Regiment of Renown", "Path to Glory Path",
    "HERO", "INFANTRY", "CAVALRY", "BEAST", "MONSTER", "WAR MACHINE",
    "MANIFESTATION", "ENDLESS SPELL", "FACTION TERRAIN", "UNIQUE",
    "WARMASTER", "WIZARD", "PRIEST", "FLY",
    "CHAOS", "ORDER", "DEATH", "DESTRUCTION",
    "SLAVES TO DARKNESS", "WARRIORS OF CHAOS", "DARKOATH", "DAEMON",
    "Ruinous Champion", "Oathsworn", "Standard Bearer",
]
CAT_IDS = {name: nr_id(f"cat-{name}") for name in CATEGORIES}
FREE_MLORE_TOGGLE_ID = nr_id("cfg-free-manifestation-lores")


def make_unit_profile(name, move, health, save, control, banish="-"):
  vals = {"Move": move, "Health": health, "Save": save, "Control": control, "Banishment": banish}
  return {
      "name": name,
      "id": nr_id(f"prof-unit-{name}"),
      "hidden": False,
      "typeId": PT_UNIT,
      "typeName": "Unit",
      "characteristics": [
          {"name": k, "$text": str(v), "typeId": char_id("unit", k)}
          for k, v in vals.items()
      ],
  }


def make_weapon_profile(parent, name, atk, hit, wnd, rnd, dmg, abil="-", rng=None):
  is_ranged = rng is not None
  pt_label = "ranged" if is_ranged else "melee"
  vals = {}
  if is_ranged:
    vals["Rng"] = rng
  vals.update({"Atk": atk, "Hit": hit, "Wnd": wnd, "Rnd": rnd, "Dmg": dmg, "Ability": abil})
  return {
      "name": name,
      "id": nr_id(f"prof-w-{parent}-{name}"),
      "hidden": False,
      "typeId": PT_RANGED if is_ranged else PT_MELEE,
      "typeName": "Ranged Weapon" if is_ranged else "Melee Weapon",
      "characteristics": [
          {"name": k, "$text": str(v), "typeId": char_id(pt_label, k)}
          for k, v in vals.items()
      ],
  }


def make_ability_profile(
    parent, name, effect, timing=None, declare="-", keywords="-", cost="-", cast_val=None
):
  if cast_val is not None:
    vals = {"Timing": timing or "Your Hero Phase", "Value": cast_val, "Declare": declare, "Effect": effect, "Keywords": keywords}
    return {
        "name": name,
        "id": nr_id(f"prof-abil-{parent}-{name}"),
        "hidden": False,
        "typeId": PT_ABIL_SPL,
        "typeName": "Ability (Spell / Prayer)",
        "characteristics": [
            {"name": k, "$text": str(v), "typeId": char_id("spell", k)}
            for k, v in vals.items()
        ],
    }
  if timing:
    vals = {"Timing": timing, "Cost": cost, "Declare": declare, "Effect": effect, "Keywords": keywords}
    return {
        "name": name,
        "id": nr_id(f"prof-abil-{parent}-{name}"),
        "hidden": False,
        "typeId": PT_ABIL_ACT,
        "typeName": "Ability (Activated)",
        "characteristics": [
            {"name": k, "$text": str(v), "typeId": char_id("activated", k)}
            for k, v in vals.items()
        ],
    }
  vals = {"Effect": effect, "Keywords": keywords}
  return {
      "name": name,
      "id": nr_id(f"prof-abil-{parent}-{name}"),
      "hidden": False,
      "typeId": PT_ABIL_PAS,
      "typeName": "Ability (Passive)",
      "characteristics": [
          {"name": k, "$text": str(v), "typeId": char_id("passive", k)}
          for k, v in vals.items()
      ],
  }


MANIFESTATION_WARSCROLLS = [
    ("Aethervoid Pendulum", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Slicing Arc", "Your Movement Phase", "Pick up to 3 enemy units moved across or passed within 1/2 inch.", "Roll a dice for each target; on a 2+, inflict mortal damage equal to the roll.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Chronomantic Cogs", "-", 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL"], [],
     [("Increase Time Flow", "Your Hero Phase", "Pick a friendly unit wholly within 12 inches.", "Add 1 to charge rolls for the target for the rest of the turn.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)"),
      ("Decrease Time Flow", "Your Hero Phase", "Pick a friendly Wizard wholly within 12 inches.", "Subtract 1 from hit rolls for attacks targeting that Wizard.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Quicksilver Swords", '12"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"],
     [("Quicksilver Blades", "melee", None, 6, "4+", "3+", 1, 2, "Crit (2 Hits)")],
     [("Dancing Blades", None, "-", "Ward rolls cannot be made for damage inflicted by this Manifestation.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Horrorghast", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"],
     [("Scream of Terror", "ranged", '10"', 6, "4+", "3+", 2, 1, "Shoot in Combat, Anti-INFANTRY (+1 Rend)"),
      ("Deathly Touch", "melee", None, 4, "4+", "4+", "-", 1, "-")],
     [("Horrifying Shriek", "Your Shooting Phase", "Pick an enemy unit targeted by shooting attacks.", "Target cannot use commands if dice roll is less than slain models.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Lauchon the Soulseeker", '12"', 10, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Traverse the Tides of Death", "Your Movement Phase", "Pick a friendly Infantry Wizard Hero within 3 inches.", "Move this Manifestation and set up target within 3 inches, inflicting 1 mortal damage.", "CORE, MOVE, MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Soulscream Bridge", "-", 7, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL"], [],
     [("Deathly Passage", "Your Movement Phase", "Pick a friendly unit wholly within 6 inches of one part.", "Set up target wholly within 6 inches of the other part and >9 inches from enemies.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Shards of Valagharr", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Phantasmal Translocation", "Your Movement Phase", "Pick one part of this Manifestation.", "Set up that part wholly within 9 inches of the other part and >3 inches from enemies.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Malevolent Maelstrom", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Morbid Detonation", "End of Any Turn", "If this Manifestation has 6 maelstrom points, pick units within 9 inches.", "Roll a dice for each target; on a 2+, inflict mortal damage equal to roll, then destroy.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Purple Sun of Shyish", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Pull of the Nadiri", None, "-", "Subtract 1 from save rolls for units within 3 inches.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)"),
      ("End-of-the-Line", "Your Movement Phase", "Pick up to 3 enemy units passed across.", "Roll D3 for each target; on a 2+, inflict mortal damage equal to roll.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Soulsnare Shackles", "-", 6, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL"], [],
     [("Ensnaring Soul-Drain", "Your Movement Phase", "Pick an enemy unit within 9 inches.", "Disable Fly and roll D3: inflict mortal damage and reduce Move.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Suffocating Gravetide", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Pulled to the Grave", "Your Movement Phase", "Pick an enemy unit passed across.", "Roll D3: on a 2+, inflict mortal damage and reduce Move.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("The Burning Head", '12"', 6, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"],
     [("Flaming Skull", "ranged", '12"', "2D6", "4+", "3+", 1, 1, "Shoot in Combat")],
     [("Blazing Fury", "Your Shooting Phase", "-", "Allocate 1 un-wardable damage to this Manifestation after shooting.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Emerald Lifeswarm", '8"', 6, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Lifeswarm", "Your Hero Phase", "Pick a friendly unit within 6 inches.", "Heal (D3) the target unit.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Ravenak's Gnashing Jaws", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL"],
     [("Gnashing Jaws", "melee", None, 4, "4+", "3+", 1, 2, "-")],
     [("Ravening Hunger", "Any Charge Phase", "If charged, pick an enemy unit within 1 inch.", "Roll 10 dice; each 5+ inflicts 1 mortal damage.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Geminids of Uhl-Gysh", '8"', 6, "6+", "-", "7+", ["MANIFESTATION", "ENDLESS SPELL", "FLY"], [],
     [("Tendrils of Light and Shadow", None, "-", "Enemy units within 3 inches cannot use commands.", "MANIFESTATION, ENDLESS SPELL, FLY, WARD (6+)")]),
    ("Prismatic Palisade", "-", 6, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL"], [],
     [("Blinding Light", None, "-", "Blocks shooting attacks crossing this Manifestation from >12 inches.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Umbral Spellportal", "-", 6, "6+", "-", "6+", ["MANIFESTATION", "ENDLESS SPELL"], [],
     [("Arcane Passage", "Your Hero Phase", "Pick a friendly Wizard within 6 inches of one part.", "Measure spell range and visibility from the other part.", "MANIFESTATION, ENDLESS SPELL, WARD (6+)")]),
    ("Krondspine Incarnate of Ghur", '8"', 14, "4+", "-", "7+", ["MANIFESTATION", "FLY"],
     [("Amberbone Claws and Fangs", "melee", None, 6, "4+", "2+", 2, 3, "Anti-MANIFESTATION (+1 Rend)")],
     [("Wild Form", None, "-", "When banished, allocate 6 un-wardable damage instead of removing.", "MANIFESTATION, FLY"),
      ("Devourer of Magics", "End of Any Turn", "-", "Heal (6) if it destroyed an enemy Manifestation this turn.", "MANIFESTATION, FLY")]),
]


def build_manifestation_warscroll_entries():
  entries = []
  for mname, move, hp, sv, ctrl, ban, cats, weps, abils in MANIFESTATION_WARSCROLLS:
    profs = [make_unit_profile(mname, move, hp, sv, ctrl, banish=ban)]
    for w_name, w_kind, rng, atk, hit, wnd, rnd, dmg, w_abil in weps:
      profs.append(make_weapon_profile(mname, w_name, atk, hit, wnd, rnd, dmg, abil=w_abil, rng=rng if w_kind == "ranged" else None))
    for a_name, timing, decl, eff, kw in abils:
      profs.append(make_ability_profile(mname, a_name, eff, timing=timing, declare=decl, keywords=kw))
    entries.append({
        "id": nr_id(f"manif-warscroll-{mname}"),
        "name": mname,
        "type": "unit",
        "hidden": False,
        "import": True,
        "costs": [{"name": "pts", "typeId": COST_PTS, "value": 0}],
        "categoryLinks": [{
            "id": nr_id(f"cl-manif-{mname}-{c}"),
            "name": c,
            "hidden": False,
            "primary": c == "MANIFESTATION",
            "targetId": CAT_IDS[c],
        } for c in cats],
        "profiles": profs,
    })
  return entries


def build_universal_manifestation_lores():
  lores = [
      ("Aetherwrought Machineries", 0, ["Aethervoid Pendulum", "Chronomantic Cogs", "Quicksilver Swords"],
       [("Summon Aethervoid Pendulum", 6), ("Summon Chronomantic Cogs", 6), ("Summon Quicksilver Swords", 6)]),
      ("Forbidden Power", 20, ["Horrorghast", "Lauchon the Soulseeker", "Soulscream Bridge", "Shards of Valagharr"],
       [("Summon Horrorghast", 6), ("Summon Lauchon the Soulseeker", 6), ("Summon Soulscream Bridge", 6), ("Summon Shards of Valagharr", 6)]),
      ("Morbid Conjuration", 20, ["Malevolent Maelstrom", "Purple Sun of Shyish", "Soulsnare Shackles", "Suffocating Gravetide"],
       [("Summon Malevolent Maelstrom", 6), ("Summon Purple Sun of Shyish", 7), ("Summon Soulsnare Shackles", 6), ("Summon Suffocating Gravetide", 6)]),
      ("Primal Energy", 10, ["The Burning Head", "Emerald Lifeswarm", "Ravenak's Gnashing Jaws"],
       [("Summon The Burning Head", 6), ("Summon Emerald Lifeswarm", 6), ("Summon Ravenak's Gnashing Jaws", 6)]),
      ("Twilit Sorceries", 0, ["Geminids of Uhl-Gysh", "Prismatic Palisade", "Umbral Spellportal"],
       [("Summon Geminids of Uhl-Gysh", 6), ("Summon Prismatic Palisade", 6), ("Summon Umbral Spellportal", 6)]),
      ("Krondspine Incarnate", 0, ["Krondspine Incarnate of Ghur"],
       [("Summon Krondspine Incarnate of Ghur", 8)]),
  ]
  entries = []
  for lore_name, pts, ws_names, spells in lores:
    profs = [
        make_ability_profile(
            lore_name, s_name,
            "Set up the summoned Manifestation wholly within 12 inches of the caster and >9 inches from enemies.",
            timing="Your Hero Phase",
            declare="Pick a friendly Wizard to cast this spell (2D6).",
            keywords="Spell, Summon",
            cast_val=c_val,
        )
        for s_name, c_val in spells
    ]
    nested_links = [{
        "id": nr_id(f"el-lore-ws-{lore_name}-{ws}"),
        "name": ws,
        "hidden": False,
        "type": "selectionEntry",
        "targetId": nr_id(f"manif-warscroll-{ws}"),
        "constraints": [
            {"id": nr_id(f"c-lore-ws-min-{lore_name}-{ws}"), "type": "min", "value": 1, "field": "selections", "scope": "parent"},
            {"id": nr_id(f"c-lore-ws-max-{lore_name}-{ws}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"},
        ],
    } for ws in ws_names]
    sub_upgrades = []
    modifiers = []
    if pts > 0:
      local_toggle = nr_id(f"upg-free-lore-{lore_name}")
      sub_upgrades.append({
          "id": local_toggle,
          "name": "Free Lore Override (Path to Glory / Narrative - 0 pts)",
          "type": "upgrade",
          "hidden": False,
          "constraints": [{"id": nr_id(f"c-free-lore-{lore_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
      })
      modifiers.append({
          "field": COST_PTS,
          "type": "set",
          "value": 0,
          "conditionGroups": [{
              "type": "or",
              "conditions": [
                  {"childId": local_toggle, "field": "selections", "scope": "self", "type": "atLeast", "value": 1},
                  {"childId": FREE_MLORE_TOGGLE_ID, "field": "selections", "includeChildForces": True, "includeChildSelections": True, "scope": "roster", "type": "atLeast", "value": 1},
              ],
          }],
      })
    entries.append({
        "id": nr_id(f"univ-mlore-{lore_name}"),
        "name": f"Manifestation Lore: {lore_name}",
        "type": "upgrade",
        "hidden": False,
        "import": True,
        "costs": [{"name": "pts", "typeId": COST_PTS, "value": pts}],
        "constraints": [{"id": nr_id(f"c-max-1-mlore-{lore_name}"), "type": "max", "value": 1, "field": "selections", "scope": "roster"}],
        "categoryLinks": [{"id": nr_id(f"cl-mlore-{lore_name}"), "name": "Manifestation Lore", "primary": True, "targetId": CAT_IDS["Manifestation Lore"]}],
        "profiles": profs,
        "selectionEntries": sub_upgrades,
        "entryLinks": nested_links,
        "modifiers": modifiers,
    })
  return entries


def build_regiments_of_renown():
  regiments = [
      ("Gotrek Gurnisson", 360, "Gotrek Gurnisson", "Order Regiment of Renown."),
      ("The Blacktalons", 340, "Neave Blacktalon", "Order Regiment of Renown."),
      ("Saviours of Cinderfall", 270, "Callis and Toll", "Order Regiment of Renown."),
      ("Elthwin's Thorns", 250, "Elthwin", "Order Regiment of Renown."),
      ("Fjori's Flamebearers", 250, "Fjori", "Order Regiment of Renown."),
      ("Norgrimm's Rune Throng", 300, "Norgrimm", "Order Regiment of Renown."),
      ("Brand's Oathbound", 210, "Gunnar Brand", "Chaos Regiment of Renown."),
      ("Hargax's Pit-Beasts", 240, "Hargax", "Chaos Regiment of Renown."),
      ("Goroan Scions", 240, "Ogroid Myrmidon", "Chaos Regiment of Renown."),
      ("Lord Skaldior's Chosen", 320, "Lord Skaldior", "Chaos Regiment of Renown."),
      ("The Coven of Thryx", 270, "Thryx", "Chaos Regiment of Renown."),
      ("Phulgoth's Shudderhood", 240, "Phulgoth", "Chaos Regiment of Renown."),
      ("Veremord's Shamblers", 200, "Veremord", "Death Regiment of Renown."),
      ("The Sorrowmourn Choir", 270, "Lady Olynder", "Death Regiment of Renown."),
      ("Liche's Hand", 310, "Arkhan retinue", "Death Regiment of Renown."),
      ("Braggit's Bottle-snatchaz", 200, "Braggit", "Destruction Regiment of Renown."),
      ("Big Grikk's Kruleshots", 220, "Big Grikk", "Destruction Regiment of Renown."),
  ]
  return [{
      "id": nr_id(f"ror-{r_name}"),
      "name": f"Regiment of Renown: {r_name}",
      "type": "unit",
      "hidden": False,
      "import": True,
      "costs": [{"name": "pts", "typeId": COST_PTS, "value": pts}],
      "categoryLinks": [{"id": nr_id(f"cl-ror-{r_name}"), "name": "Regiment of Renown", "primary": True, "targetId": CAT_IDS["Regiment of Renown"]}],
      "profiles": [make_ability_profile(r_name, f"Regiment Composition ({leader})", desc, timing="Army Composition")],
  } for r_name, pts, leader, desc in regiments]


def build_universal_ptg_paths():
  paths = [
      ("Path of the Leader (Hero)", "Aspiring: Inspiring Leader | Elite: Coordinated Muster | Mighty: Titan of War | Legendary: Legendary Warlord"),
      ("Path of the Cavalier (Hero / Unit)", "Aspiring: Thunderous Charge | Elite: Swift Flankers | Mighty: Linebreakers | Legendary: Ride to Glory"),
      ("Path of the Mage / Priest (Hero)", "Aspiring: Arcane Conduit | Elite: Eldritch Ward | Mighty: Master of Sorcery | Legendary: Ascendant Caster"),
      ("Path of the Warrior (Unit)", "Aspiring: Veteran Fighters | Elite: Stalwart Defenders | Mighty: Relentless Assault | Legendary: Champions of the Realms"),
      ("Path of the Behemoth / Sentinel (Unit)", "Aspiring: Unyielding Hide | Elite: Ground-shaking Stride | Mighty: Apex Predator | Legendary: Living Cataclysm"),
  ]
  return [{
      "id": nr_id(f"univ-ptg-{p_name}"),
      "name": p_name,
      "type": "upgrade",
      "hidden": False,
      "import": True,
      "categoryLinks": [{"id": nr_id(f"cl-ptg-path-{p_name}"), "name": "Path to Glory Path", "primary": True, "targetId": CAT_IDS["Path to Glory Path"]}],
      "profiles": [make_ability_profile("Path to Glory", p_name, p_desc)],
      "selectionEntryGroups": [{
          "id": nr_id(f"grp-ranks-{p_name}"),
          "name": "Progression Rank",
          "hidden": False,
          "constraints": [{"id": nr_id(f"c-rank-{p_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
          "selectionEntries": [{"id": nr_id(f"rank-{p_name}-{r}"), "name": f"Rank: {r}", "type": "upgrade", "hidden": False} for r in ["Aspiring", "Elite", "Mighty", "Legendary"]],
      }],
      "selectionEntries": [
          {"id": nr_id(f"ptg-renown-{p_name}"), "name": "Renown Point", "type": "upgrade", "hidden": False, "costs": [{"name": "Renown", "typeId": COST_RENOWN, "value": 1}]},
          {"id": nr_id(f"ptg-scar-{p_name}"), "name": "Battle Wound / Battle Scar", "type": "upgrade", "hidden": False},
      ],
  } for p_name, p_desc in paths]


def make_regiment_cat_links(force_prefix: str, unit_cats: list):
  return [
      {
          "id": nr_id(f"{force_prefix}-cl-HERO"),
          "name": "HERO",
          "targetId": CAT_IDS["HERO"],
          "constraints": [
              {"id": nr_id(f"{force_prefix}-c-h-min"), "type": "min", "value": 1, "field": "selections", "scope": "force"},
              {"id": nr_id(f"{force_prefix}-c-h-max"), "type": "max", "value": 1, "field": "selections", "scope": "force"},
          ],
      }
  ] + [
      {"id": nr_id(f"{force_prefix}-cl-{c}"), "name": c, "targetId": CAT_IDS[c]}
      for c in unit_cats
      if c != "HERO"
  ]


def build_gamesystem():
  unit_cat_links = ["HERO", "INFANTRY", "CAVALRY", "BEAST", "MONSTER", "WAR MACHINE"]

  cfg_entries = [{
      "id": FREE_MLORE_TOGGLE_ID,
      "name": "Manifestation Lores: Free (Path to Glory / Narrative)",
      "type": "upgrade",
      "hidden": False,
      "import": True,
      "constraints": [{"id": nr_id("c-cfg-free-mlore-max"), "type": "max", "value": 1, "field": "selections", "scope": "roster"}],
      "categoryLinks": [{"id": nr_id("cl-cfg-free-mlore"), "name": "Configuration", "primary": True, "targetId": CAT_IDS["Configuration"]}],
  }]

  shared_entries = (
      cfg_entries
      + build_manifestation_warscroll_entries()
      + build_universal_manifestation_lores()
      + build_regiments_of_renown()
      + build_universal_ptg_paths()
  )
  entry_links = [{
      "id": nr_id(f"el-gs-{se['id']}"),
      "name": se["name"],
      "hidden": False,
      "type": "selectionEntry",
      "targetId": se["id"],
  } for se in shared_entries]

  return {
      "gameSystem": {
          "id": GS_ID,
          "name": "Warhammer Age of Sigmar",
          "revision": 2,
          "battleScribeVersion": "2.03",
          "xmlns": "http://www.battlescribe.net/schema/gameSystemSchema",
          "costTypes": [
              {"id": COST_PTS, "name": "pts", "defaultCostLimit": 2000, "hidden": False},
              {"id": COST_GLORY, "name": "Glory Points", "defaultCostLimit": -1, "hidden": False},
              {"id": COST_RENOWN, "name": "Renown", "defaultCostLimit": -1, "hidden": False},
              {"id": COST_DESTINY, "name": "Destiny Points", "defaultCostLimit": -1, "hidden": False},
          ],
          "profileTypes": [
              {"id": PT_UNIT, "name": "Unit", "characteristicTypes": [{"id": char_id("unit", k), "name": k} for k in ["Move", "Health", "Save", "Control", "Banishment"]]},
              {"id": PT_MELEE, "name": "Melee Weapon", "characteristicTypes": [{"id": char_id("melee", k), "name": k} for k in ["Atk", "Hit", "Wnd", "Rnd", "Dmg", "Ability"]]},
              {"id": PT_RANGED, "name": "Ranged Weapon", "characteristicTypes": [{"id": char_id("ranged", k), "name": k} for k in ["Rng", "Atk", "Hit", "Wnd", "Rnd", "Dmg", "Ability"]]},
              {"id": PT_ABIL_ACT, "name": "Ability (Activated)", "characteristicTypes": [{"id": char_id("activated", k), "name": k} for k in ["Timing", "Cost", "Declare", "Effect", "Keywords"]]},
              {"id": PT_ABIL_PAS, "name": "Ability (Passive)", "characteristicTypes": [{"id": char_id("passive", k), "name": k} for k in ["Effect", "Keywords"]]},
              {"id": PT_ABIL_SPL, "name": "Ability (Spell / Prayer)", "characteristicTypes": [{"id": char_id("spell", k), "name": k} for k in ["Timing", "Value", "Declare", "Effect", "Keywords"]]},
          ],
          "categoryEntries": [{"id": cid, "name": cname, "hidden": False} for cname, cid in CAT_IDS.items()],
          "sharedRules": [
              {"id": nr_id("rule-crit-2-hits"), "name": "Crit (2 Hits)", "description": "Scores 2 hits on a critical hit instead of 1."},
              {"id": nr_id("rule-crit-auto-wound"), "name": "Crit (Auto-wound)", "description": "Automatically wounds on a critical hit."},
              {"id": nr_id("rule-crit-mortal"), "name": "Crit (Mortal)", "description": "Inflicts mortal damage equal to weapon Damage on a critical hit and the attack sequence ends."},
              {"id": nr_id("rule-companion"), "name": "Companion", "description": "Not affected by friendly abilities unless Companion weapons are explicitly specified."},
              {"id": nr_id("rule-shoot-in-combat"), "name": "Shoot in Combat", "description": "Can make shooting attacks even while in combat."},
          ],
          "sharedSelectionEntries": shared_entries,
          "entryLinks": entry_links,
          "forceEntries": [
              {
                  "id": nr_id("force-matched-play"),
                  "name": "Matched Play: General's Handbook",
                  "hidden": False,
                  "categoryLinks": [
                      {"id": nr_id("cl-mp-config"), "name": "Configuration", "targetId": CAT_IDS["Configuration"]},
                      {"id": nr_id("cl-mp-comp"), "name": "Army Composition", "targetId": CAT_IDS["Army Composition"]},
                      {"id": nr_id("cl-mp-mlore"), "name": "Manifestation Lore", "targetId": CAT_IDS["Manifestation Lore"]},
                      {"id": nr_id("cl-mp-manif"), "name": "MANIFESTATION", "targetId": CAT_IDS["MANIFESTATION"]},
                      {"id": nr_id("cl-mp-ror"), "name": "Regiment of Renown", "targetId": CAT_IDS["Regiment of Renown"]},
                      {"id": nr_id("cl-mp-terr"), "name": "FACTION TERRAIN", "targetId": CAT_IDS["FACTION TERRAIN"]},
                  ],
                  "forceEntries": [
                      {
                          "id": nr_id("force-generals-regiment"),
                          "name": "General's Regiment",
                          "hidden": False,
                          "constraints": [{"id": nr_id("c-gen-reg-max"), "type": "max", "value": 1, "field": "forces", "scope": "parent"}],
                          "categoryLinks": make_regiment_cat_links("gen-reg", unit_cat_links),
                      },
                      {
                          "id": nr_id("force-regiment"),
                          "name": "Regiment",
                          "hidden": False,
                          "constraints": [{"id": nr_id("c-reg-max"), "type": "max", "value": 4, "field": "forces", "scope": "parent"}],
                          "categoryLinks": make_regiment_cat_links("reg", unit_cat_links),
                      },
                      {
                          "id": nr_id("force-auxiliaries"),
                          "name": "Auxiliary Units",
                          "hidden": False,
                          "categoryLinks": [{"id": nr_id(f"cl-aux-{c}"), "name": c, "targetId": CAT_IDS[c]} for c in unit_cat_links],
                      },
                  ],
              },
              {
                  "id": nr_id("force-ptg-ascension"),
                  "name": "Path to Glory: Ascension / Ravaged Coast",
                  "hidden": False,
                  "categoryLinks": [
                      {"id": nr_id(f"cl-ptg-{c}"), "name": c, "targetId": CAT_IDS[c]}
                      for c in ["Configuration", "Army Composition", "Order of Battle", "Manifestation Lore", "MANIFESTATION", "Regiment of Renown", "Path to Glory Path", "FACTION TERRAIN"] + unit_cat_links
                  ],
              },
          ],
      }
  }


if __name__ == "__main__":
  with open(GS_FILENAME, "w", encoding="utf-8") as f:
    json.dump(build_gamesystem(), f, indent=2)
  print(f"Compiled {GS_FILENAME} in root folder.")