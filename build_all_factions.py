import json
import os
from build_repo import (
    CAT_IDS,
    COST_DESTINY,
    COST_GLORY,
    COST_PTS,
    COST_RENOWN,
    GS_FILENAME,
    GS_ID,
    build_gamesystem,
    make_ability_profile,
    make_unit_profile,
    make_weapon_profile,
    nr_id,
)

ALL_FACTIONS = {
    "Cities of Sigmar": {
        "alliance": "ORDER",
        "battle_traits": [
            ("Officer's Orders", "Your Hero Phase", "Issue Orders from friendly Heroes to friendly units wholly within 12 inches."),
            ("Fortify Position", "Deployment Phase", "Friendly Castelite units gain +1 to save rolls while stationary."),
        ],
        "formations": [
            ("Fortress-city Defenders", "Add 1 to save rolls for friendly Castelite Infantry contesting objectives you control."),
            ("Ironweld Guild Army", "Add 3 inches to Range for friendly Ironweld ranged weapons."),
            ("Collegiate Arcane Expedition", "Add 1 to casting rolls for friendly Collegiate Arcane Wizards."),
            ("Dawnbringer Crusade", "Add 2 inches to Move for friendly Cities of Sigmar units in battle round 1."),
        ],
        "traits": [("Master of Ballistics", "Add 1 to hit rolls for shooting attacks wholly within 12 inches.")],
        "artefacts": [("Sacred Tome", "This Hero gains Wizard (1) or +1 to casting/chanting rolls.")],
        "lores": [("Spells of the Collegiate Arcane", "Speed of Twin-tailed Comet", 7, "Target friendly unit within 12 inches can run and still shoot/charge.")],
        "terrain": None,
        "units": [
            {"name": "Tahlia Vedra, Lioness of the Parch", "pts": 310, "move": '12"', "health": 12, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "ORDER", "CITIES OF SIGMAR"], "reinforce": False, "weapons": [("Warmaster's Blade", 5, "3+", "3+", 2, 2, "Crit (Mortal)", None), ("Infernadine's Claws and Maw", 5, "4+", "2+", 2, 3, "Companion", None)], "abilities": [("Unparalleled Tactician", "Pick up to 3 friendly units within 18 inches to receive Orders.", "Your Hero Phase")]},
            {"name": "Freeguild Marshal and Relic Envoy", "pts": 110, "move": '5"', "health": 5, "save": "3+", "control": 2, "primary": "HERO", "cats": ["HERO", "INFANTRY", "ORDER", "CITIES OF SIGMAR"], "reinforce": False, "weapons": [("Master-forged Longsword", 5, "3+", "3+", 1, 2, "-", None)], "abilities": [("Rousing Speech", "Friendly Freeguild units wholly within 12 inches add 3 to control scores.", None)]},
            {"name": "Freeguild Steelhelms", "pts": 90, "move": '5"', "health": 1, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "CITIES OF SIGMAR"], "reinforce": True, "weapons": [("Steelhelm Weapon", 2, "4+", "4+", 0, 1, "-", None)], "abilities": [("Consecrate the Land", "Contested objectives controlled by this unit gain Ward (6+).", "End of Any Turn")]},
        ],
    },
    "Daughters of Khaine": {
        "alliance": "ORDER",
        "battle_traits": [
            ("Blood Rites", "Start of Battle Round", "Cumulative army-wide buffs across battle rounds."),
            ("Fanatical Faith", "Passive", "Friendly Daughters of Khaine units have Ward (6+)."),
        ],
        "formations": [
            ("Slaughter Troupe", "Friendly Witch Aelves and Sisters of Slaughter can retreat and still charge."),
            ("Scáthborn Coven", "Add 1 to hit rolls for Blood Stalkers and Melusai."),
            ("Shadow Patrol", "Friendly Khinerai and Doomfire Warlocks gain +2 inches Move."),
            ("Cauldron Guard", "Add 1 to chanting rolls for friendly Daughters of Khaine Priests."),
        ],
        "traits": [("Zealous Orator", "Return up to D6 slain models to a friendly Witch Aelves or Sisters of Slaughter unit within 12 inches.")],
        "artefacts": [("Crown of Woe", "Subtract 3 from control scores of enemy units within 12 inches.")],
        "lores": [("Lore of Shadows", "Mindrazor", 7, "Target friendly unit within 12 inches gains +1 Rend and +1 Damage on the charge.")],
        "terrain": None,
        "units": [
            {"name": "Morathi-Khaine", "pts": 760, "move": '8"', "health": 6, "save": "4+", "control": 2, "primary": "HERO", "cats": ["HERO", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "ORDER", "DAUGHTERS OF KHAINE"], "reinforce": False, "weapons": [("Heartrender", 3, "3+", "3+", 2, 2, "-", None)], "abilities": [("One Soul, Two Bodies", "Transfers damage to The Shadow Queen (max 3 per turn).", None)]},
            {"name": "The Shadow Queen", "pts": 0, "move": '14"', "health": 12, "save": "4+", "control": 5, "primary": "MONSTER", "cats": ["MONSTER", "UNIQUE", "FLY", "ORDER", "DAUGHTERS OF KHAINE"], "reinforce": False, "weapons": [("Heartrender and Envenomed Tail", 6, "3+", "2+", 2, 3, "Crit (Mortal)", None)], "abilities": [("Iron Heart of Khaine", "Cannot suffer more than 3 damage points in a single turn.", None)]},
            {"name": "Witch Aelves", "pts": 110, "move": '6"', "health": 1, "save": "6+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "DAUGHTERS OF KHAINE"], "reinforce": True, "weapons": [("Sacrificial Knives", 3, "3+", "4+", 0, 1, "Crit (Auto-wound)", None)], "abilities": [("Frenzied Fervour", "Add 1 to wound rolls while within 12 inches of a Daughters of Khaine Hero.", None)]},
        ],
    },
    "Fyreslayers": {
        "alliance": "ORDER",
        "battle_traits": [("Ur-Gold Runes", "Start of Battle Round", "Activate 1 of 6 Ur-Gold Runes per battle.")],
        "formations": [
            ("Warrior Kinband", "Add 1 to wound rolls for Vulkite Berzerkers."),
            ("Lords of the Lodge", "Friendly Auric Hearthguard and Hearthguard Berzerkers gain +1 Attack near a Hero."),
            ("Scales of Vulcatrix", "Add 2 to Health for Magmadroth units."),
            ("Forge Brethren", "Add 1 to save rolls near Battlesmiths or Runemasters."),
        ],
        "traits": [("Ash-beard", "This Hero gains Priest (1) or +1 to chanting rolls.")],
        "artefacts": [("Draught of Magmalt Ale", "Once per battle, double melee Attacks for one phase.")],
        "lores": [("Prayer of the Grimwrath", "Wrath of Vulcatrix", 4, "Empowers Magmic Invocations and adds +1 Rend.")],
        "terrain": ("Magmic Battleforge", 0, "Grants +1 chanting near the Battleforge."),
        "units": [
            {"name": "Auric Runefather on Magmadroth", "pts": 350, "move": '10"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "ORDER", "FYRESLAYERS"], "reinforce": False, "weapons": [("Latchkey Grandaxe", 5, "3+", "2+", 2, 3, "-", None), ("Magmadroth's Claws and Horns", 5, "4+", "2+", 2, 2, "Companion", None)], "abilities": [("Lodge Leader", "Friendly Fyreslayers wholly within 12 inches gain +1 Attack.", "Any Combat Phase")]},
            {"name": "Vulkite Berzerkers with Fyresteel Handaxes", "pts": 130, "move": '4"', "health": 2, "save": "6+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "FYRESLAYERS"], "reinforce": True, "weapons": [("Pair of Fyresteel Handaxes", 3, "4+", "3+", 0, 1, "Crit (2 Hits)", None)], "abilities": [("Berserk Fury", "Fight on death on a 4+.", None)]},
        ],
    },
    "Idoneth Deepkin": {
        "alliance": "ORDER",
        "battle_traits": [("Tides of Death", "Start of Battle Round", "Cycle Low Tide, Flood Tide, High Tide, and Ebb Tide.")],
        "formations": [
            ("Akhelian Beastmasters", "Add 1 to hit rolls for Companion weapons of Leviadons, Allopexes, and Guard."),
            ("Namarti Corps", "Return D3 slain models to Namarti units in your Hero Phase."),
            ("Soul-raid Ambushers", "Deploy units in reserve in the Ethersea."),
            ("Isharann Council", "Add 1 to casting rolls for Isharann Wizards."),
        ],
        "traits": [("Lord of Storm and Tide", "Add 3 to control scores wholly within 12 inches.")],
        "artefacts": [("Armour of the Cythai", "Enemy units cannot make critical hits against this Hero.")],
        "lores": [("Lore of the Deeps", "Steed of Tides", 6, "Teleport a friendly Idoneth Hero >9 inches from enemies.")],
        "terrain": ("Gloomtide Shipwreck", 0, "Grants Ward (6+) to friendly Idoneth units within 6 inches."),
        "units": [
            {"name": "Eidolon of Mathlann, Aspect of the Sea", "pts": 350, "move": '12"', "health": 12, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "WIZARD", "FLY", "ORDER", "IDONETH DEEPKIN"], "reinforce": False, "weapons": [("Psi-trident and Deep-sea Cloak", 5, "3+", "3+", 1, 2, "-", None)], "abilities": [("Dormant Energies", "Add 1 to casting rolls per friendly Idoneth unit within 12 inches (max +3).", None)]},
            {"name": "Namarti Thralls", "pts": 110, "move": '6"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "IDONETH DEEPKIN"], "reinforce": True, "weapons": [("Lanmari Blade", 3, "3+", "4+", 1, 1, "Anti-INFANTRY (+1 Rend)", None)], "abilities": [("Sweeping Blows", "Add 1 to Damage against 10+ model Infantry units.", None)]},
        ],
    },
    "Kharadron Overlords": {
        "alliance": "ORDER",
        "battle_traits": [("Sky-fleets & Aether-gold", "Any Phase", "Embark Skyfarers in Skyvessels and spend Aether-gold.")],
        "formations": [
            ("Iron Sky Attack Squadron", "Friendly Frigates and Gunhaulers gain +2 inches Move."),
            ("Grundstok Expeditionary Force", "Add 1 to hit rolls for Grundstok shooting."),
            ("Endrineers Guild", "Heal D3+1 damage on Skyvessels."),
            ("Pioneer Outriders", "Friendly Skywardens and Endrinriggers can retreat and shoot."),
        ],
        "traits": [("Endrinmaestro", "Add 3 inches to Range of Skyvessel weapons within 12 inches.")],
        "artefacts": [("Spell in a Bottle", "Once per battle, automatically cast a Universal Endless Spell.")],
        "lores": [],
        "terrain": None,
        "units": [
            {"name": "Brokk Grungsson, Lord-Magnate of Barak-Nar", "pts": 270, "move": '12"', "health": 8, "save": "3+", "control": 2, "primary": "HERO", "cats": ["HERO", "UNIQUE", "FLY", "ORDER", "KHARADRON OVERLORDS"], "reinforce": False, "weapons": [("Magnate's Charter Pistol & Aetherblaster", 6, "3+", "3+", 1, 1, "Shoot in Combat", '12"'), ("Grundstok Saw", 5, "3+", "3+", 2, 2, "-", None)], "abilities": [("First Rule of Grungsson", "Friendly Skyfarers within 12 inches add 1 melee Attack on charge.", "Any Charge Phase")]},
            {"name": "Arkanaut Company", "pts": 100, "move": '4"', "health": 1, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "KHARADRON OVERLORDS"], "reinforce": True, "weapons": [("Privateer Pistol and Light Skyhook", 2, "4+", "4+", 0, 1, "-", '12"'), ("Arkanaut Cutter", 2, "4+", "4+", 0, 1, "-", None)], "abilities": [("Glory-hog", "Add 1 to hit when targeting units contesting an objective.", None)]},
        ],
    },
    "Lumineth Realm-lords": {
        "alliance": "ORDER",
        "battle_traits": [("Facets of War", "Start of Battle Round", "Select Vanari, Scinari, Alarith, or Hurakan facets.")],
        "formations": [
            ("Vanari Battlehost", "Vanari units gain +1 to hit when within 1 inch of another Vanari unit."),
            ("Scinari Council", "Add 1 to casting and unbinding rolls for Scinari Wizards."),
            ("Alarith Temple", "Alarith units ignore 1 point of Rend and gain +1 Damage vs Monsters."),
            ("Hurakan Temple", "Add 2 inches to Move for Hurakan units."),
        ],
        "traits": [("Masterful Tactician", "Re-deploy 1 friendly Lumineth unit up to D6 inches.")],
        "artefacts": [("Silver Wand", "Add 1 to casting rolls for this Hero.")],
        "lores": [("Lore of Hysh", "Speed of Hysh", 6, "Target friendly Lumineth unit within 12 inches doubles its Move.")],
        "terrain": ("Shrine Luminor", 0, "Garrisons a Hero and grants a 0 CP command."),
        "units": [
            {"name": "Archmage Teclis and Celennar", "pts": 590, "move": '12"', "health": 16, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "ORDER", "LUMINETH REALM-LORDS"], "reinforce": False, "weapons": [("Sword of Teclis", 4, "3+", "3+", 2, 2, "-", None), ("Celennar's Claws and Horns", 4, "4+", "3+", 1, 2, "Companion", None)], "abilities": [("Archmage of Hysh", "Casts up to 4 spells per phase at automatic value 10.", "Your Hero Phase")]},
            {"name": "Vanari Auralan Wardens", "pts": 140, "move": '6"', "health": 1, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "LUMINETH REALM-LORDS"], "reinforce": True, "weapons": [("Warden's Pike", 2, "3+", "4+", 1, 1, "Anti-CAVALRY (+1 Rend)", None)], "abilities": [("Sunmetal Weapons", "Scores Crit (Mortal) on a 5+ when empowered.", None)]},
        ],
    },
    "Seraphon": {
        "alliance": "ORDER",
        "battle_traits": [("The Great Plan", "Start of Battle Round", "Choose Itzl, Quetzl, Sotek, or Tepok.")],
        "formations": [
            ("Sunclaw Starhost", "Saurus units deal D3 mortal damage on a 3+ at end of Combat."),
            ("Shadowstrike Starhost", "Skink units gain +1 to hit against unactivated targets."),
            ("Thunderquake Starhost", "Add 2 to Health for Seraphon Monsters."),
            ("Eternal Starhost", "Slann Wizards can teleport a Seraphon unit >9 inches from enemies."),
        ],
        "traits": [("Being of the Stars", "Ignore negative modifiers to save rolls.")],
        "artefacts": [("Incandescent Rectrices", "Heal 6 damage once per battle when slain.")],
        "lores": [("Lore of Celestial Manipulation", "Comet's Call", 7, "Inflict D3 mortal damage on up to D3 enemy units.")],
        "terrain": ("Realmshaper Engine", 0, "Deals D3 mortal damage near terrain features."),
        "units": [
            {"name": "Lord Kroak", "pts": 430, "move": '5"', "health": 12, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "ORDER", "SERAPHON"], "reinforce": False, "weapons": [("Spectral Claws", 4, "4+", "4+", 1, 1, "-", None)], "abilities": [("Deliverance of Itza", "Casts up to 3 times per phase.", "Your Hero Phase")]},
            {"name": "Saurus Warriors", "pts": 160, "move": '5"', "health": 2, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "SERAPHON"], "reinforce": True, "weapons": [("Celestite Club or Spear", 2, "3+", "3+", 1, 1, "-", None)], "abilities": [("Ordered Cohort", "Add 1 to save rolls while contesting a controlled objective.", None)]},
        ],
    },
    "Sylvaneth": {
        "alliance": "ORDER",
        "battle_traits": [
            ("Places of Power & Awakened Wyldwoods", "Your Hero Phase", "Heal D3 near Wyldwoods and walk the hidden paths."),
            ("Strike and Fade", "End of Any Turn", "Teleport to a Wyldwood after fighting."),
        ],
        "formations": [
            ("Outcasts", "Spite-Revenants and Dryads gain +1 Attack."),
            ("Forest Folk", "Tree-Revenants and Kurnoth Hunters gain +1 to hit near Wyldwoods."),
            ("Lords of the Clan", "Add 2 to Health for Treelords, Durthu, and Alarielle."),
            ("Free Spirits", "Add 2 inches to Move for Revenant Seekers and Spiterider Lancers."),
        ],
        "traits": [("Spellsinger", "Measure spell ranges from any friendly Awakened Wyldwood.")],
        "artefacts": [("Seed of Rebirth", "Return to play with D6 health when slain.")],
        "lores": [("Lore of the Deepwood", "Treesong", 6, "Target friendly unit within 12 inches gains +1 Rend.")],
        "terrain": ("Awakened Wyldwood", 0, "Provides cover, healing, and teleportation."),
        "units": [
            {"name": "Alarielle the Everqueen", "pts": 680, "move": '14"', "health": 16, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "ORDER", "SYLVANETH"], "reinforce": False, "weapons": [("Spear of Kurnoth", 4, "3+", "3+", 2, 3, "Crit (Mortal)", '12"'), ("Talon of Dwindling", 4, "3+", "2+", 2, 3, "-", None)], "abilities": [("Lifebloom", "Heals 2D6 on Alarielle and D3 on Sylvaneth units.", "Your Hero Phase")]},
            {"name": "Tree-Revenants", "pts": 110, "move": '5"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "SYLVANETH"], "reinforce": True, "weapons": [("Enchanted Blade", 2, "3+", "4+", 1, 1, "-", None)], "abilities": [("Waypipes", "Teleport anywhere >9 inches from enemies.", "Your Movement Phase")]},
        ],
    },
    "Stormcast Eternals": {
        "alliance": "ORDER",
        "battle_traits": [
            ("Scions of the Storm", "Deployment Phase", "Deploy units in the Celestial Realm."),
            ("Their Finest Hour", "Any Combat Phase", "Once per battle per unit, +1 to wound and +1 to save."),
        ],
        "formations": [
            ("Thunderhead Host", "Warrior Chamber units gain +1 to hit near non-Warrior Chamber units."),
            ("Sentinels of the Bleak Citadels", "Ruination Chamber units gain Ward (5+) in combat."),
            ("Vanguard Wing", "Vanguard Chamber units teleport in your Movement Phase."),
            ("Lightning Echelon", "Extremis Chamber units gain Strike-first on a 4+ when charging."),
        ],
        "traits": [("Shock and Awe", "Subtract 1 from hit rolls on arrival turn.")],
        "artefacts": [("Null Pendant", "Automatically unbind a spell or banish a Manifestation.")],
        "lores": [("Lore of the Storm", "Azyrite Halo", 6, "Deals 1 mortal damage on unmodified save rolls of 6.")],
        "terrain": ("Stormreach Portal", 0, "Teleports friendly Stormcast Infantry units."),
        "units": [
            {"name": "Yndrasta, the Celestial Spear", "pts": 340, "move": '12"', "health": 8, "save": "3+", "control": 2, "primary": "HERO", "cats": ["HERO", "UNIQUE", "FLY", "ORDER", "STORMCAST ETERNALS"], "reinforce": False, "weapons": [("Thengavar", 1, "3+", "2+", 2, "D6", "Anti-MONSTER (+1 Rend)", '12"'), ("Blade of the High Heavens", 5, "3+", "3+", 2, 3, "Anti-MONSTER (+1 Rend)", None)], "abilities": [("Prime Huntress", "Doubles Damage against enemy Monsters.", None)]},
            {"name": "Liberators", "pts": 110, "move": '5"', "health": 2, "save": "3+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "ORDER", "STORMCAST ETERNALS"], "reinforce": True, "weapons": [("Warhammer / Grandhammer", 2, "3+", "3+", 1, 1, "Crit (Mortal)", None)], "abilities": [("Stalwart Defenders", "Add 3 to control scores while contesting a controlled objective.", None)]},
        ],
    },
    "Slaves to Darkness": {
        "alliance": "CHAOS",
        "battle_traits": [
            ("Eye of the Gods", "Deployment Phase", "Gain Dark Apotheosis points in combat and on enemy objectives."),
            ("Pledge to Chaos", "Your Hero Phase", "Pledge units to Khorne, Tzeentch, Nurgle, or Slaanesh."),
            ("Dark Apotheosis", "Any Hero Phase", "Ascend Heroes with 8+ Dark Apotheosis points."),
        ],
        "formations": [
            ("Godswrath Warband", "Defile objectives to inflict D3 mortal damage on enemies on a 2+."),
            ("Legion of Chaos", "Add 2 to control scores contesting enemy-territory objectives."),
            ("Darkoath Horde", "Return destroyed non-Hero Darkoath units at half strength on a 3+."),
            ("Despoilers", "Empowers Monsters and Pledge synergies."),
        ],
        "traits": [("Favoured of the Pantheon", "Start with D3 Dark Apotheosis points.")],
        "artefacts": [("Infernal Puppet", "Inflict D3 mortal damage on an enemy Wizard casting spells.")],
        "lores": [("Lore of the Damned", "Daemonic Power", 6, "Friendly Warriors of Chaos unit within 12 inches gains +1 to hit and +1 to wound.")],
        "terrain": ("Nexus Chaotica", 0, "Gains dark power tokens per Hero Phase."),
        "units": [
            {"name": "Archaon, the Everchosen", "pts": 870, "move": '12"', "health": 20, "save": "3+", "control": 10, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "CHAOS", "SLAVES TO DARKNESS", "WARRIORS OF CHAOS"], "reinforce": False, "weapons": [("The Slayer of Kings", 6, "3+", "2+", 2, 3, "Crit (Mortal)", None), ("Dorghar's Claws and Three Heads", 9, "4+", "2+", 2, 3, "Companion", None)], "abilities": [("The Eye of Sheerian", "Dictates priority roll for next battle round.", "Your Hero Phase")]},
            {"name": "Be'lakor, the Dark Master", "pts": 440, "move": '14"', "health": 14, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "CHAOS", "SLAVES TO DARKNESS", "DAEMON"], "reinforce": False, "weapons": [("The Blade of Shadows", 5, "3+", "2+", 2, 3, "Crit (Mortal)", None), ("Fell Claws", 4, "3+", "3+", 1, 2, "-", None)], "abilities": [("The Dark Master", "Shuts down an enemy unit's abilities on a 3+.", "Once Per Battle, Enemy Hero Phase")]},
            {"name": "Chaos Warriors", "pts": 200, "move": '5"', "health": 2, "save": "3+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "SLAVES TO DARKNESS", "WARRIORS OF CHAOS"], "reinforce": True, "weapons": [("Rune-etched Weapons", 2, "3+", "3+", 1, 1, "Crit (Auto-wound)", None)], "abilities": [("Bringers of Desolation", "Add 1 melee Attack while contesting a controlled objective.", None)]},
        ],
    },
    "Blades of Khorne": {
        "alliance": "CHAOS",
        "battle_traits": [("Blood Tithe", "Any Phase", "Gain Blood Tithe points when units are destroyed.")],
        "formations": [
            ("Bloodbound Warhorde", "Add 1 to wound rolls for charging Bloodbound units."),
            ("Murderhost", "Add 2 inches to Move for Khorne Daemon units."),
            ("Brass Stampede", "Skullcrushers and Bloodcrushers deal D3 mortal damage on charge."),
            ("Khornate Legion", "Synergizes Mortal and Daemon units."),
        ],
        "traits": [("Favoured of Khorne", "Gain 1 bonus Blood Tithe point on a 3+.")],
        "artefacts": [("Halo of Blood", "This Hero has Strike-first.")],
        "lores": [("Blood Blessings of Khorne", "Bronzed Flesh", 4, "Target friendly Khorne unit within 16 inches gains +1 to save.")],
        "terrain": ("Skull Altar", 0, "Grants +1 chanting to Khorne Priests within 8 inches."),
        "units": [
            {"name": "Skarbrand", "pts": 470, "move": '8"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "CHAOS", "BLADES OF KHORNE", "DAEMON"], "reinforce": False, "weapons": [("Slaughter and Carnage", 8, "3+", "2+", 2, 3, "Crit (Mortal)", None)], "abilities": [("Total Carnage", "Devastating melee output.", None)]},
            {"name": "Bloodletters", "pts": 200, "move": '6"', "health": 2, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "BLADES OF KHORNE", "DAEMON"], "reinforce": True, "weapons": [("Hellblade", 2, "3+", "3+", 1, 1, "Crit (Mortal)", None)], "abilities": [("Decapitating Blow", "Crit (Mortal) on 5+ when charging.", None)]},
        ],
    },
    "Disciples of Tzeentch": {
        "alliance": "CHAOS",
        "battle_traits": [
            ("Masters of Destiny", "Start of Battle", "Roll 9 Destiny Dice at the start of the battle."),
            ("Burning Wyrdflame", "End of Any Turn", "Wyrdflame attacks inflict Burning damage."),
        ],
        "formations": [
            ("Wyrdflame Host", "Subtract 1 from wound rolls targeting friendly units from Burning enemies."),
            ("Arcanite Cabal", "Arcanite Wizards cast an extra spell per phase."),
            ("Changehost", "Daemons near a Locus of Change gain Ward (5+)."),
            ("Tzaangor Coven", "Add 1 to hit and wound for Tzaangors near a Shaman."),
        ],
        "traits": [("Cult Demagogue", "Doubles on casting rolls generate extra Destiny Dice.")],
        "artefacts": [("Nine-eyed Tome", "Re-roll 1 casting or unbinding roll per turn.")],
        "lores": [("Lore of Change", "Bolt of Tzeentch", 7, "Inflict D6 mortal damage on a unit within 18 inches.")],
        "terrain": None,
        "units": [
            {"name": "Kairos Fateweaver", "pts": 440, "move": '12"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "CHAOS", "DISCIPLES OF TZEENTCH", "DAEMON"], "reinforce": False, "weapons": [("Staff of Tomorrow", 4, "3+", "3+", 1, 2, "-", None), ("Beaks and Talons", 5, "4+", "3+", 1, 2, "-", None)], "abilities": [("Oracle of Eternity", "Change any single dice roll once per battle.", "Any Phase")]},
            {"name": "Pink Horrors", "pts": 150, "move": '6"', "health": 1, "save": "6+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "DISCIPLES OF TZEENTCH", "DAEMON"], "reinforce": True, "weapons": [("Magical Flames", 2, "4+", "4+", 0, 1, "Shoot in Combat", '18"')], "abilities": [("Split and Split Again", "Splits into smaller horrors when slain.", None)]},
        ],
    },
    "Maggotkin of Nurgle": {
        "alliance": "CHAOS",
        "battle_traits": [
            ("Blessed by the Plaguefather", "Passive", "All friendly Maggotkin units have Ward (5+)."),
            ("Diseased", "End of Any Turn", "Diseased units suffer D3 mortal damage at the end of turns."),
        ],
        "formations": [
            ("Plague Cyst", "Diseased enemies suffer +1 mortal damage in combat with Rotbringers."),
            ("Tallyband of Nurgle", "Return D3 slain Plaguebearers or Nurglings."),
            ("Affliction Cyst", "Pusgoyle Blightlords and Plague Drones gain +2 inches Move."),
            ("Gardeners of Nurgle", "Enemy units within 6 inches of Gnarlmaws become Diseased."),
        ],
        "traits": [("Grandfather's Blessing", "Add 1 to ward rolls (to 4+) once per battle.")],
        "artefacts": [("The Witherstave", "Enemy units within 7 inches cannot score critical hits.")],
        "lores": [("Lore of Malignance", "Fleshy Abundance", 7, "Target friendly Nurgle unit within 12 inches gains +1 Health.")],
        "terrain": ("Feculent Gnarlmaw", 0, "Spreads Disease and enables run & charge."),
        "units": [
            {"name": "Great Unclean One", "pts": 480, "move": '5"', "health": 20, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "WIZARD", "CHAOS", "MAGGOTKIN OF NURGLE", "DAEMON"], "reinforce": False, "weapons": [("Bilesword / Doomsday Bell", 5, "3+", "2+", 2, 3, "-", None)], "abilities": [("Reverberating Summons", "Return a destroyed Daemon unit at half strength on a 3+.", "Your Hero Phase")]},
            {"name": "Putrid Blightkings", "pts": 190, "move": '4"', "health": 3, "save": "3+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "MAGGOTKIN OF NURGLE"], "reinforce": True, "weapons": [("Blighted Weapons", 4, "3+", "3+", 1, 1, "Crit (2 Hits)", None)], "abilities": [("Relentless Tacklers", "Add 3 to control scores when contesting an objective.", None)]},
        ],
    },
    "Hedonites of Slaanesh": {
        "alliance": "CHAOS",
        "battle_traits": [("Temptation Dice & Euphoric Killers", "Any Phase", "Offer Temptation Dice and spend Depravity Points.")],
        "formations": [
            ("Seeker Cavalcade", "Seekers can run and still charge."),
            ("Invaders", "Slaanesh Heroes gain +1 Attack and +1 to wound vs Heroes."),
            ("Pretenders", "General issues the same command up to 3 times."),
            ("Sybarite Blade-carnival", "Add 1 to hit rolls for Sybarite Infantry."),
        ],
        "traits": [("Glory Hog", "Generate 2 Depravity Points when an enemy unit is destroyed within 12 inches.")],
        "artefacts": [("Icon of Infinite Excess", "Friendly Slaanesh units within 12 inches gain +1 Attack once per battle.")],
        "lores": [("Lore of Pain and Pleasure", "Pavane of Slaanesh", 7, "Roll dice equal to target Move; each 5+ deals 1 mortal damage.")],
        "terrain": ("Fane of Slaanesh", 0, "Grants casting/chanting and wound bonuses."),
        "units": [
            {"name": "Keeper of Secrets", "pts": 440, "move": '14"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "WIZARD", "CHAOS", "HEDONITES OF SLAANESH", "DAEMON"], "reinforce": False, "weapons": [("Elegant Greatblade", 6, "3+", "2+", 2, 3, "Crit (2 Hits)", None)], "abilities": [("Dark Temptations", "Inflicts D3 mortal damage or grants Temptation Dice.", "Any Combat Phase")]},
            {"name": "Blissbarb Archers", "pts": 150, "move": '6"', "health": 1, "save": "6+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "HEDONITES OF SLAANESH"], "reinforce": True, "weapons": [("Blissbarb Bow", 2, "3+", "4+", 1, 1, "Crit (Auto-wound)", '18"')], "abilities": [("Light-footed Killers", "Can run and still shoot.", None)]},
        ],
    },
    "Skaven": {
        "alliance": "CHAOS",
        "battle_traits": [
            ("Always Three Clawsteps Ahead", "End of Any Turn", "Free D6 inches move or retreat once per turn."),
            ("The Lurking Vermintide", "Deployment Phase", "Deploy in Gnawhole tunnels."),
        ],
        "formations": [
            ("Claw-horde", "Add 1 to Rend for charging Verminus units."),
            ("Warpcog Convocation", "Overcharge Skryre weapons."),
            ("Fleshmeld Menagerie", "Heal D3 on Moulder Monsters."),
            ("Virulent Procession", "Add 1 to chanting for Pestilens Priests."),
        ],
        "traits": [("Scurry Away", "Retreat instead of fighting when picked.")],
        "artefacts": [("Skavenbrew", "+1 Attack on a friendly Infantry unit for D3 mortal damage.")],
        "lores": [("Lore of Ruin", "Skitterleap", 6, "Teleport a Skaven Hero >9 inches from enemies.")],
        "terrain": ("Gnawhole", 0, "Teleportation tunnels and clanrat reinforcements."),
        "units": [
            {"name": "Vizzik Skour, Prophet of the Horned Rat", "pts": 420, "move": '8"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "PRIEST", "CHAOS", "SKAVEN", "DAEMON"], "reinforce": False, "weapons": [("Gnawstaff & Scourging Claws", 7, "3+", "3+", 2, 2, "Crit (Mortal)", None)], "abilities": [("Death Frenzy", "Chants powerful prayers.", "Your Hero Phase")]},
            {"name": "Clanrats", "pts": 150, "move": '6"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "SKAVEN"], "reinforce": True, "weapons": [("Rusty Blade", 2, "4+", "4+", 0, 1, "Crit (Auto-wound)", None)], "abilities": [("Seething Swarm", "Return D3 slain models at end of turn.", "End of Any Turn")]},
        ],
    },
    "Helsmiths of Hashut": {
        "alliance": "CHAOS",
        "battle_traits": [("Daemonic Power & Desolation", "Your Hero Phase", "Fuel war machines and dark smithing blessings.")],
        "formations": [
            ("Forge-host of Hashut", "Add 1 to hit for Hashut War Machines."),
            ("Bull-centaur Stampede", "Bull Centaurs gain +1 Rend and +1 Damage on charge."),
            ("Ziggurat Guard", "Add 1 to save rolls for Infernal Cohort."),
            ("Daemonsmith Conclave", "Add 1 to casting/ritual rolls for Daemonsmiths."),
        ],
        "traits": [("Master Daemonsmith", "Heal D3+1 damage on a friendly War Machine within 6 inches.")],
        "artefacts": [("Gauntlets of Hashut", "Deals D3 mortal damage in an 8-inch blast.")],
        "lores": [("Lore of Hashut", "Ash Storm", 7, "Target enemy unit within 18 inches suffers -1 to hit and -3 inches Move.")],
        "terrain": None,
        "units": [
            {"name": "Daemonsmith Lord on Great Taurus", "pts": 340, "move": '12"', "health": 14, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "WIZARD", "FLY", "CHAOS", "HELSMITHS OF HASHUT"], "reinforce": False, "weapons": [("Darkforged Warhammer", 5, "3+", "3+", 2, 2, "-", None), ("Great Taurus's Blazing Horns", 5, "4+", "2+", 2, 3, "Companion", None)], "abilities": [("Blazing Body", "Deals mortal damage at end of turn.", "End of Any Turn")]},
            {"name": "Infernal Cohort", "pts": 150, "move": '4"', "health": 2, "save": "3+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "CHAOS", "HELSMITHS OF HASHUT"], "reinforce": True, "weapons": [("Darkforged Glaive", 2, "3+", "3+", 1, 1, "Anti-CAVALRY (+1 Rend)", None)], "abilities": [("Shieldwall of Hashut", "Ward (5+) against mortal damage.", None)]},
        ],
    },
    "Flesh-eater Courts": {
        "alliance": "DEATH",
        "battle_traits": [
            ("Noble Deeds", "Any Phase", "Earn up to 6 Noble Deeds points to muster units."),
            ("Feeding Frenzy", "Passive", "+1 melee Attacks near Heroes with 6 Noble Deeds."),
        ],
        "formations": [
            ("Cannibal Court", "Add 1 to hit for Crypt Ghouls and Cryptguard."),
            ("Royal Menagerie", "Add 2 to Health for Terrorgheists and Zombie Dragons."),
            ("Knightly Echelon", "Knights and Horrors/Flayers gain +1 Rend on charge."),
            ("Lords of the Manor", "Return 1 extra model on Muster abilities."),
        ],
        "traits": [("Cruel Taskmaster", "Reduce Noble Deeds cost of Muster by 1.")],
        "artefacts": [("Charnel Vestments", "This Hero gains Priest (1).")],
        "lores": [("Lore of Madness", "Deranged Transformation", 6, "Target friendly unit within 12 inches gains +2 inches Move and +1 to wound.")],
        "terrain": ("Charnel Throne", 0, "Garrisons an Abhorrant Hero and generates Noble Deeds."),
        "units": [
            {"name": "Ushoran, Mortarch of Delusion", "pts": 470, "move": '8"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "DEATH", "FLESH-EATER COURTS"], "reinforce": False, "weapons": [("Skull-topped Sceptre and Claws", 7, "3+", "2+", 2, 3, "Crit (2 Hits)", None)], "abilities": [("Shroudcage Fragment", "Enemy units within 12 inches have Strike-last on a 3+.", "Any Combat Phase")]},
            {"name": "Cryptguard", "pts": 120, "move": '6"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DEATH", "FLESH-EATER COURTS"], "reinforce": True, "weapons": [("Cursed Halberd or Blade", 2, "3+", "4+", 1, 1, "-", None)], "abilities": [("Royal Bodyguard", "Heroes wholly within 3 inches gain Ward (5+).", None)]},
        ],
    },
    "Nighthaunt": {
        "alliance": "DEATH",
        "battle_traits": [
            ("Ethereal", "Passive", "Ignore save roll modifiers for Nighthaunt units."),
            ("Aura of Dread", "Any Charge Phase", "Apply Shrieker, Stun, or Petrify debuffs."),
        ],
        "formations": [
            ("Vanishing Phantasms", "Redeploy up to 3 Nighthaunt units >9 inches from enemies."),
            ("Death Stalkers", "Nighthaunt units can run and still charge."),
            ("Procession of Death", "Add 1 to ward rolls (to 5+) for Infantry on objectives."),
            ("Hunters of the Accursed", "Add 1 to hit against enemy Heroes."),
        ],
        "traits": [("Ruler of the Spirit Hosts", "Return a destroyed non-Hero unit at half strength.")],
        "artefacts": [("Lightshard of the Harvest Moon", "+1 Attack wholly within 12 inches once per battle.")],
        "lores": [("Lore of the Underworlds", "Spectral Tether", 6, "Teleport a Hero >9 inches from enemies and heal D3.")],
        "terrain": None,
        "units": [
            {"name": "Lady Olynder, Mortarch of Grief", "pts": 300, "move": '8"', "health": 8, "save": "4+", "control": 2, "primary": "HERO", "cats": ["HERO", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "DEATH", "NIGHTHAUNT"], "reinforce": False, "weapons": [("Staff of Midnight & Banshee Handmaidens", 6, "3+", "3+", 2, 2, "Crit (Mortal)", None)], "abilities": [("No Rest for the Wicked", "Returns up to D3+1 models to Nighthaunt units.", "Your Hero Phase")]},
            {"name": "Bladegheist Revenants", "pts": 150, "move": '8"', "health": 1, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "FLY", "DEATH", "NIGHTHAUNT"], "reinforce": True, "weapons": [("Tomb Greatblade", 2, "3+", "3+", 1, 1, "-", None)], "abilities": [("Whirling Death", "+1 melee Attacks if charged this turn.", None)]},
        ],
    },
    "Ossiarch Bonereapers": {
        "alliance": "DEATH",
        "battle_traits": [("Relentless Discipline", "Any Phase", "Issue up to 5 Ossiarch Commands per battle round.")],
        "formations": [
            ("Mortek Phalanx", "+1 save for Mortek Guard and Crawlers on objectives."),
            ("Kavalos Lance", "Kavalos Deathriders gain +1 Rend and +1 Damage on charge."),
            ("Mortisan Council", "+1 casting for Mortisan Wizards."),
            ("Tithe-reaper Echelon", "+1 Attack for Harvesters and Stalkers."),
        ],
        "traits": [("Mighty Archaeossian", "Add 2 to Health and +1 to save.")],
        "artefacts": [("Lode of Saturation", "Grants Ward (5+) to a friendly Ossiarch unit within 6 inches.")],
        "lores": [("Lore of Ossian Sorcery", "Empower Nadirite Weapons", 6, "Crit (2 Hits) on a 5+ for target unit.")],
        "terrain": ("Bone-tithe Nexus", 0, "Deals mortal damage or debuffs enemy rolls."),
        "units": [
            {"name": "Katakros, Mortarch of the Necropolis", "pts": 520, "move": '5"', "health": 20, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "UNIQUE", "WARMASTER", "DEATH", "OSSIARCH BONEREAPERS"], "reinforce": False, "weapons": [("Inda-Khaat & Retinue Weapons", 10, "3+", "3+", 2, 2, "-", None)], "abilities": [("Supreme Lord of the Bonereaper Legions", "Friendly Ossiarch units within 18 inches add 1 to hit and save.", None)]},
            {"name": "Mortek Guard", "pts": 130, "move": '4"', "health": 1, "save": "4+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DEATH", "OSSIARCH BONEREAPERS"], "reinforce": True, "weapons": [("Nadirite Blade or Spear", 2, "3+", "4+", 1, 1, "Crit (2 Hits)", None)], "abilities": [("Shieldwall", "Immune to critical hits when stationary/un-charged.", None)]},
        ],
    },
    "Soulblight Gravelords": {
        "alliance": "DEATH",
        "battle_traits": [
            ("The Hunger", "End of Any Turn", "Vampires heal D3 (or D6 for Monsters) after fighting."),
            ("Endless Legions", "Your Movement Phase", "Return destroyed Deathrattle or Deadwalkers at half strength."),
        ],
        "formations": [
            ("Legion of Shyish", "Return D3+1 slain models to Summonable units."),
            ("Bacchanal of Blood", "+1 casting for Vampires and +1 wound when charging."),
            ("Deathmarch", "+1 Rend for Deathrattle units outnumbering targets."),
            ("Deathstench Drove", "+1 to hit for Deadwalkers units."),
        ],
        "traits": [("Unbending Will", "Add 3 to control scores for Summonable units within 12 inches.")],
        "artefacts": [("Orb of Enchantment", "Give an enemy Hero within 3 inches Strike-last once per battle.")],
        "lores": [("Lore of Undeath", "Vile Transference", 7, "Inflict D3 mortal damage and heal the caster.")],
        "terrain": None,
        "units": [
            {"name": "Nagash, Supreme Lord of the Undead", "pts": 880, "move": '8"', "health": 18, "save": "3+", "control": 10, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "DEATH", "SOULBLIGHT GRAVELORDS"], "reinforce": False, "weapons": [("Zefet-nebtar & Alakanash", 6, "3+", "2+", 2, 3, "Crit (Mortal)", None)], "abilities": [("Supreme Lord of the Undead", "Casts up to 8 spells per phase.", "Your Hero Phase")]},
            {"name": "Deathrattle Skeletons", "pts": 100, "move": '4"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DEATH", "SOULBLIGHT GRAVELORDS"], "reinforce": True, "weapons": [("Ancient Weapon", 2, "4+", "4+", 0, 1, "-", None)], "abilities": [("Skeleton Legion", "Return D3 slain models at start of Combat.", "Any Combat Phase")]},
        ],
    },
    "Gloomspite Gitz": {
        "alliance": "DESTRUCTION",
        "battle_traits": [
            ("The Bad Moon", "Start of Battle Round", "The Bad Moon moves across the battlefield."),
            ("Loonshrine Resurrection", "End of Your Turn", "Return destroyed units at half strength near the Loonshrine."),
        ],
        "formations": [
            ("Gloomspite Horde", "Add 3 to control scores for Moonclan Infantry."),
            ("Squigalanche", "Squigs roll 3D6 drop lowest for charges under the Bad Moon."),
            ("Troggherd", "Add 1 to hit for Troggoths and boost Regeneration."),
            ("Spiderfang Stalktribe", "Crit (Mortal) on 5+ for Spiderfang Companion weapons."),
        ],
        "traits": [("Fight Another Day", "Retreat D6 inches after attacking when picked to fight.")],
        "artefacts": [("Leering Gitshield", "Inflicts 1 mortal damage on unmodified save rolls of 6.")],
        "lores": [("Lore of the Clammy Dank", "Itchy Nuisance", 6, "Target enemy unit within 12 inches has Strike-last.")],
        "terrain": ("Bad Moon Loonshrine", 0, "Projects Bad Moon light and resurrects units."),
        "units": [
            {"name": "Skragrott, the Loonking", "pts": 220, "move": '5"', "health": 6, "save": "5+", "control": 2, "primary": "HERO", "cats": ["HERO", "UNIQUE", "WARMASTER", "WIZARD", "DESTRUCTION", "GLOOMSPITE GITZ"], "reinforce": False, "weapons": [("Da Moon Onna Stikk", 4, "3+", "3+", 2, "D3", "-", None)], "abilities": [("Babbling Wand", "Controls Bad Moon movement once per battle.", "Your Hero Phase")]},
            {"name": "Moonclan Stabbas", "pts": 140, "move": '5"', "health": 1, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DESTRUCTION", "GLOOMSPITE GITZ"], "reinforce": True, "weapons": [("Pokin' Spear or Stabba", 2, "4+", "4+", 0, 1, "-", None)], "abilities": [("Netters", "Subtract 1 from hit rolls for enemy Infantry in combat.", None)]},
        ],
    },
    "Ironjawz": {
        "alliance": "DESTRUCTION",
        "battle_traits": [
            ("Mighty Destroyers", "Your Hero Phase", "Free 3-inch move or pile-in into combat."),
            ("Ironjawz Waaagh!", "Any Combat Phase", "Once per battle, +1 Attack and +1 Rend in combat."),
        ],
        "formations": [
            ("Ironfist", "Add 1 to charge rolls for Ironjawz units."),
            ("Grunta Stampede", "Gore-gruntas and Maw-gruntas deal D3 mortal damage on charge."),
            ("Weirdfist", "+1 casting for Weirdnob Shamans per 10 Ironjawz models within 12 inches."),
            ("Brutefist", "+1 to hit against 3+ Health targets."),
        ],
        "traits": [("Hulking Brute", "Deals D3 mortal damage on a 2+ after charging.")],
        "artefacts": [("Destroyer", "Once per battle, add 3 to melee Damage.")],
        "lores": [("Lore of the Weird", "Da Great Big Green Hand of Gork", 7, "Teleport an Ironjawz unit >9 inches from enemies.")],
        "terrain": ("Bossrokk Tower", 0, "Empowers Shamans and extends Waaagh! range."),
        "units": [
            {"name": "Gordrakk, the Fist of Gork", "pts": 430, "move": '10"', "health": 18, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "FLY", "DESTRUCTION", "IRONJAWZ"], "reinforce": False, "weapons": [("Smasha and Kunnin'", 8, "3+", "2+", 2, 3, "Crit (2 Hits)", None)], "abilities": [("Voice of Gork", "Calls an army-wide Waaagh!.", "Once Per Battle, Any Combat Phase")]},
            {"name": "Ardboyz", "pts": 180, "move": '4"', "health": 2, "save": "3+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DESTRUCTION", "IRONJAWZ"], "reinforce": True, "weapons": [("Ardboy Choppa or Stikka", 2, "3+", "3+", 1, 1, "Anti-CAVALRY (+1 Rend)", None)], "abilities": [("Shield Bash", "Deals mortal damage on a 4+ at end of Combat.", "End of Any Turn")]},
        ],
    },
    "Kruleboyz": {
        "alliance": "DESTRUCTION",
        "battle_traits": [("Dirty Tricks", "Any Phase", "Activate Dirty Tricks across phases.")],
        "formations": [
            ("Kruleboyz Klaw", "-1 to hit for shooting targeting Infantry >12 inches away."),
            ("Trophy Finga", "+1 to hit for Killbows and Boltboyz."),
            ("Middul-finga", "+1 to Dirty Trick rolls."),
            ("Swamphorde Bullies", "+1 to wound for Gutrippaz near a Killaboss."),
        ],
        "traits": [("Backstabba", "+2 melee Attacks against already engaged enemies.")],
        "artefacts": [("Mork's Eye Pebble", "Ward (5+) wholly within 12 inches once per battle.")],
        "lores": [("Lore of the Swamp", "Choking Mist", 6, "Target enemy unit within 18 inches suffers -1 melee Attacks.")],
        "terrain": ("Skaregob Totem", 0, "Amplifies Dirty Tricks."),
        "units": [
            {"name": "Gobsprakk, the Mouth of Mork", "pts": 330, "move": '12"', "health": 16, "save": "4+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "WIZARD", "FLY", "DESTRUCTION", "KRULEBOYZ"], "reinforce": False, "weapons": [("Gork's Toof & Killabeak's Talons", 7, "3+", "3+", 2, 2, "Crit (Mortal)", None)], "abilities": [("Screaming Mandrake", "Punishes enemy spellcasting.", "Enemy Hero Phase")]},
            {"name": "Gutrippaz", "pts": 150, "move": '5"', "health": 2, "save": "5+", "control": 1, "primary": "INFANTRY", "cats": ["INFANTRY", "DESTRUCTION", "KRULEBOYZ"], "reinforce": True, "weapons": [("Wicked Stikka or Hacka", 2, "4+", "3+", 0, 1, "Crit (Mortal)", None)], "abilities": [("Scare Taktikz", "-1 to hit for enemy Infantry in combat.", None)]},
        ],
    },
    "Ogor Mawtribes": {
        "alliance": "DESTRUCTION",
        "battle_traits": [
            ("Trampling Charge", "Any Charge Phase", "Deal mortal damage after charging."),
            ("Ravenous Brutes", "Passive", "+2 inches Move when not in combat; +1 to hit in combat."),
        ],
        "formations": [
            ("Meatfist", "+1 to Trampling Charge mortal damage rolls for Gutbusters."),
            ("Beastclaw Raiders", "+2 inches Move for Beastclaw Monsters and Cavalry."),
            ("Blackpowder Fanatics", "+1 to hit for Leadbelchers and Ironblasters."),
            ("Prophets of the Gulping God", "+1 chanting for Butchers and Slaughtermasters."),
        ],
        "traits": [("Touched by the Everwinter", "This Hero gains Priest (1).")],
        "artefacts": [("Gruesome Trophy Rack", "+1 to hit vs Monsters and Heroes within 12 inches.")],
        "lores": [("Lore of Maw-magic", "Voracious Maw", 7, "Inflict D3 mortal damage repeatedly on a 4+.")],
        "terrain": ("Great Mawpot", 0, "Heals friendly Ogors."),
        "units": [
            {"name": "Frostlord on Stonehorn", "pts": 360, "move": '12"', "health": 16, "save": "3+", "control": 5, "primary": "HERO", "cats": ["HERO", "MONSTER", "DESTRUCTION", "OGOR MAWTRIBES"], "reinforce": False, "weapons": [("Frost Spear", 4, "3+", "3+", 2, 2, "Charge (+1 Damage)", None), ("Stonehorn's Horns and Hooves", 6, "3+", "2+", 2, 3, "Companion, Charge (+1 Damage)", None)], "abilities": [("Earth-shattering Charge", "Ward (5+) and heavy charge impact.", None)]},
            {"name": "Ogor Gluttons", "pts": 230, "move": '6"', "health": 4, "save": "5+", "control": 2, "primary": "INFANTRY", "cats": ["INFANTRY", "DESTRUCTION", "OGOR MAWTRIBES"], "reinforce": True, "weapons": [("Ogor Club or Blade", 4, "4+", "2+", 1, 2, "-", None)], "abilities": [("Beast-smashers", "+1 Damage against Monsters.", None)]},
        ],
    },
    "Sons of Behemat": {
        "alliance": "DESTRUCTION",
        "battle_traits": [
            ("Mightier Makes Rightier", "Passive", "High Control scores for Gargants."),
            ("Timberrr!", "When Slain", "Falling Mega-Gargants crush units underneath."),
        ],
        "formations": [
            ("Taker Tribe", "+1 control score and steal enemy Artefacts."),
            ("Breaker Tribe", "+1 Damage vs Faction Terrain and units in cover."),
            ("Stomper Tribe", "+1 Damage vs 10+ model Infantry."),
            ("Boss Tribe", "+1 to hit for Mancrushers near General Mega-Gargants."),
        ],
        "traits": [("Extremely Bitter", "+1 to hit and wound when damaged by 10+.")],
        "artefacts": [("Glowy Lantern", "This Hero gains Wizard (1).")],
        "lores": [],
        "terrain": None,
        "units": [
            {"name": "King Brodd", "pts": 520, "move": '10"', "health": 40, "save": "4+", "control": 20, "primary": "HERO", "cats": ["HERO", "MONSTER", "UNIQUE", "WARMASTER", "PRIEST", "DESTRUCTION", "SONS OF BEHEMAT"], "reinforce": False, "weapons": [("Obelisk of Tor Crania", 5, "3+", "2+", 2, 4, "-", None)], "abilities": [("Power of Behemat", "Chants prayers for Gargants.", "Your Hero Phase")]},
            {"name": "Mancrusher Gargant", "pts": 160, "move": '8"', "health": 12, "save": "5+", "control": 5, "primary": "MONSTER", "cats": ["MONSTER", "DESTRUCTION", "SONS OF BEHEMAT"], "reinforce": False, "weapons": [("Massive Club", 4, "4+", "3+", 1, 2, "-", None)], "abilities": [("Stuff 'Em In Me Bag", "Slays 1-Health models on a 4+.", "Any Combat Phase")]},
        ],
    },
}


def ensure_all_categories(gs_dict):
  existing = {c["name"] for c in gs_dict["gameSystem"]["categoryEntries"]}
  for f_name, f_data in ALL_FACTIONS.items():
    kw = f_name.upper()
    if kw not in CAT_IDS:
      CAT_IDS[kw] = nr_id(f"cat-{kw}")
    if kw not in existing:
      gs_dict["gameSystem"]["categoryEntries"].append({"id": CAT_IDS[kw], "name": kw, "hidden": False})
      existing.add(kw)
    for u in f_data["units"]:
      for c in u["cats"]:
        if c not in CAT_IDS:
          CAT_IDS[c] = nr_id(f"cat-{c}")
        if c not in existing:
          gs_dict["gameSystem"]["categoryEntries"].append({"id": CAT_IDS[c], "name": c, "hidden": False})
          existing.add(c)


def build_ptg_group(faction_name, unit_name, is_hero=False):
  paths = (
      [
          ("Path of the Leader", "Aspiring -> Elite -> Mighty -> Legendary"),
          ("Path of the Cavalier", "Aspiring -> Elite -> Mighty -> Legendary"),
          ("Path of the Mage / Priest", "Aspiring -> Elite -> Mighty -> Legendary"),
          (f"Path of the {faction_name} Champion", "Aspiring -> Elite -> Mighty -> Legendary"),
      ]
      if is_hero
      else [
          ("Path of the Warrior", "Aspiring -> Elite -> Mighty -> Legendary"),
          ("Path of the Cavalier", "Aspiring -> Elite -> Mighty -> Legendary"),
          ("Path of the Behemoth / Sentinel", "Aspiring -> Elite -> Mighty -> Legendary"),
          (f"Path of {faction_name} Glory", "Aspiring -> Elite -> Mighty -> Legendary"),
      ]
  )
  return {
      "id": nr_id(f"grp-ptg-{faction_name}-{unit_name}"),
      "name": "Path to Glory (Paths, Renown & Battle Scars)",
      "hidden": False,
      "collapsible": True,
      "selectionEntries": [
          {
              "id": nr_id(f"ptg-ren-{faction_name}-{unit_name}"),
              "name": "Renown Points",
              "type": "upgrade",
              "costs": [{"name": "Renown", "typeId": COST_RENOWN, "value": 1}],
          },
          {
              "id": nr_id(f"ptg-scar-{faction_name}-{unit_name}"),
              "name": "Battle Wounds / Battle Scars",
              "type": "upgrade",
          },
      ],
      "selectionEntryGroups": [{
          "id": nr_id(f"grp-paths-{faction_name}-{unit_name}"),
          "name": "Unit Path",
          "constraints": [{"id": nr_id(f"c-path-{faction_name}-{unit_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
          "selectionEntries": [{
              "id": nr_id(f"path-{faction_name}-{unit_name}-{p[0]}"),
              "name": p[0],
              "type": "upgrade",
              "profiles": [make_ability_profile(unit_name, p[0], p[1])],
              "selectionEntries": [{
                  "id": nr_id(f"rank-{faction_name}-{unit_name}-{p[0]}-{r}"),
                  "name": f"Rank: {r}",
                  "type": "upgrade",
                  "constraints": [{"id": nr_id(f"c-rk-{faction_name}-{unit_name}-{p[0]}-{r}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
              } for r in ["Aspiring", "Elite", "Mighty", "Legendary"]],
          } for p in paths],
      }],
  }


def build_faction_catalogue(faction_name, f_data):
  f_kw = faction_name.upper()
  shared_entries = []
  entry_links = []

  bt_profiles = [make_ability_profile(faction_name, bt[0], bt[2], timing=bt[1]) for bt in f_data["battle_traits"]]
  form_entries = [{
      "id": nr_id(f"bf-{faction_name}-{fm[0]}"),
      "name": fm[0],
      "type": "upgrade",
      "profiles": [make_ability_profile(fm[0], fm[0], fm[1])],
  } for fm in f_data["formations"]]
  lore_entries = [{
      "id": nr_id(f"lore-{faction_name}-{lr[0]}-{lr[1]}"),
      "name": f"{lr[0]}: {lr[1]}",
      "type": "upgrade",
      "profiles": [make_ability_profile(lr[0], lr[1], lr[3], timing="Your Hero Phase", keywords="Spell / Prayer", cast_val=lr[2])],
  } for lr in f_data["lores"]]

  army_groups = [{
      "id": nr_id(f"grp-bf-{faction_name}"),
      "name": "Battle Formations",
      "constraints": [
          {"id": nr_id(f"c-bf-min-{faction_name}"), "type": "min", "value": 1, "field": "selections", "scope": "parent"},
          {"id": nr_id(f"c-bf-max-{faction_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"},
      ],
      "selectionEntries": form_entries,
  }]
  if lore_entries:
    army_groups.append({
        "id": nr_id(f"grp-lore-{faction_name}"),
        "name": "Faction Spell / Prayer Lore",
        "constraints": [{"id": nr_id(f"c-lr-max-{faction_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
        "selectionEntries": lore_entries,
    })

  army_rules_entry = {
      "id": nr_id(f"army-rules-{faction_name}"),
      "name": f"{faction_name}: Battle Traits, Formations & Lores",
      "type": "upgrade",
      "hidden": False,
      "import": True,
      "categoryLinks": [{"id": nr_id(f"cl-ar-{faction_name}"), "name": "Army Composition", "primary": True, "targetId": CAT_IDS["Army Composition"]}],
      "profiles": bt_profiles,
      "selectionEntryGroups": army_groups,
      "selectionEntries": [{
          "id": nr_id(f"ptg-glory-{faction_name}"),
          "name": "Path to Glory: Glory Points Tracker",
          "type": "upgrade",
          "costs": [{"name": "Glory Points", "typeId": COST_GLORY, "value": 1}],
      }],
  }
  shared_entries.append(army_rules_entry)
  entry_links.append({"id": nr_id(f"el-ar-{faction_name}"), "name": army_rules_entry["name"], "hidden": False, "type": "selectionEntry", "targetId": army_rules_entry["id"]})

  if f_data.get("terrain"):
    t_name, t_pts, t_desc = f_data["terrain"]
    t_entry = {
        "id": nr_id(f"terrain-{faction_name}-{t_name}"),
        "name": t_name,
        "type": "unit",
        "hidden": False,
        "import": True,
        "costs": [{"name": "pts", "typeId": COST_PTS, "value": t_pts}],
        "categoryLinks": [
            {"id": nr_id(f"cl-t-main-{t_name}"), "name": "FACTION TERRAIN", "primary": True, "targetId": CAT_IDS["FACTION TERRAIN"]},
            {"id": nr_id(f"cl-t-all-{t_name}"), "name": f_data["alliance"], "primary": False, "targetId": CAT_IDS[f_data["alliance"]]},
            {"id": nr_id(f"cl-t-fac-{t_name}"), "name": f_kw, "primary": False, "targetId": CAT_IDS[f_kw]},
        ],
        "profiles": [make_unit_profile(t_name, "-", 10, "4+", "-"), make_ability_profile(t_name, t_name, t_desc, timing="Your Hero Phase")],
    }
    shared_entries.append(t_entry)
    entry_links.append({"id": nr_id(f"el-t-{t_name}"), "name": t_name, "hidden": False, "type": "selectionEntry", "targetId": t_entry["id"]})

  for u in f_data["units"]:
    uname = u["name"]
    is_hero = u["primary"] == "HERO"
    is_unique = "UNIQUE" in u["cats"]

    profs = [make_unit_profile(uname, u["move"], u["health"], u["save"], u["control"])]
    for w in u["weapons"]:
      profs.append(make_weapon_profile(uname, w[0], w[1], w[2], w[3], w[4], w[5], abil=w[6], rng=w[7]))
    for a in u["abilities"]:
      profs.append(make_ability_profile(uname, a[0], a[2], timing=a[1]))

    sub_entries = []
    modifiers = []
    if u.get("reinforce"):
      reinf_id = nr_id(f"reinf-{faction_name}-{uname}")
      sub_entries.append({"id": reinf_id, "name": "Reinforced", "type": "upgrade", "constraints": [{"id": nr_id(f"c-reinf-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}]})
      modifiers.append({"field": COST_PTS, "type": "multiply", "value": 2, "conditions": [{"childId": reinf_id, "field": "selections", "scope": "self", "type": "atLeast", "value": 1}]})
    if is_hero:
      sub_entries.append({"id": nr_id(f"gen-{faction_name}-{uname}"), "name": "General", "type": "upgrade", "constraints": [{"id": nr_id(f"c-gen-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}]})

    sub_groups = []
    if is_hero and not is_unique:
      sub_groups.extend([
          {
              "id": nr_id(f"grp-ht-{faction_name}-{uname}"),
              "name": "Heroic Traits",
              "constraints": [{"id": nr_id(f"c-ht-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
              "selectionEntries": [{"id": nr_id(f"ht-{faction_name}-{uname}-{t[0]}"), "name": t[0], "type": "upgrade", "profiles": [make_ability_profile(uname, t[0], t[1])]} for t in f_data["traits"]],
          },
          {
              "id": nr_id(f"grp-art-{faction_name}-{uname}"),
              "name": "Artefacts of Power",
              "constraints": [{"id": nr_id(f"c-art-{faction_name}-{uname}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"}],
              "selectionEntries": [{"id": nr_id(f"art-{faction_name}-{uname}-{a[0]}"), "name": a[0], "type": "upgrade", "profiles": [make_ability_profile(uname, a[0], a[1])]} for a in f_data["artefacts"]],
          },
      ])
    if not is_unique:
      sub_groups.append(build_ptg_group(faction_name, uname, is_hero=is_hero))

    u_entry = {
        "id": nr_id(f"unit-{faction_name}-{uname}"),
        "name": uname,
        "type": "unit",
        "hidden": False,
        "import": True,
        "costs": [
            {"name": "pts", "typeId": COST_PTS, "value": u["pts"]},
            {"name": "Glory Points", "typeId": COST_GLORY, "value": 0},
            {"name": "Renown", "typeId": COST_RENOWN, "value": 0},
        ],
        "categoryLinks": [{"id": nr_id(f"cl-{faction_name}-{uname}-{c}"), "name": c, "hidden": False, "primary": c == u["primary"], "targetId": CAT_IDS[c]} for c in u["cats"]],
        "profiles": profs,
        "selectionEntries": sub_entries,
        "selectionEntryGroups": sub_groups,
        "modifiers": modifiers,
    }
    shared_entries.append(u_entry)
    entry_links.append({"id": nr_id(f"el-{faction_name}-{uname}"), "name": uname, "hidden": False, "type": "selectionEntry", "targetId": u_entry["id"]})

  anvil_name = f"Anvil of Apotheosis: {faction_name} Hero"
  anvil_entry = {
      "id": nr_id(f"anvil-{faction_name}"),
      "name": anvil_name,
      "type": "unit",
      "hidden": False,
      "import": True,
      "costs": [
          {"name": "pts", "typeId": COST_PTS, "value": 0},
          {"name": "Destiny Points", "typeId": COST_DESTINY, "value": 0},
      ],
      "categoryLinks": [
          {"id": nr_id(f"cl-anv-hero-{faction_name}"), "name": "HERO", "primary": True, "targetId": CAT_IDS["HERO"]},
          {"id": nr_id(f"cl-anv-all-{faction_name}"), "name": f_data["alliance"], "primary": False, "targetId": CAT_IDS[f_data["alliance"]]},
          {"id": nr_id(f"cl-anv-fac-{faction_name}"), "name": f_kw, "primary": False, "targetId": CAT_IDS[f_kw]},
      ],
      "profiles": [make_unit_profile(anvil_name, '5"', 5, "4+", 2)],
      "selectionEntryGroups": [
          {
              "id": nr_id(f"grp-anv-tier-{faction_name}"),
              "name": "Destiny Point Limit",
              "constraints": [
                  {"id": nr_id(f"c-anv-min-{faction_name}"), "type": "min", "value": 1, "field": "selections", "scope": "parent"},
                  {"id": nr_id(f"c-anv-max-{faction_name}"), "type": "max", "value": 1, "field": "selections", "scope": "parent"},
              ],
              "selectionEntries": [
                  {"id": nr_id(f"anv-15-{faction_name}"), "name": "Aspiring Champion (15 Destiny Pts / 120 pts)", "type": "upgrade", "costs": [{"name": "pts", "typeId": COST_PTS, "value": 120}]},
                  {"id": nr_id(f"anv-25-{faction_name}"), "name": "Aspiring Lord (25 Destiny Pts / 200 pts)", "type": "upgrade", "costs": [{"name": "pts", "typeId": COST_PTS, "value": 200}]},
                  {"id": nr_id(f"anv-35-{faction_name}"), "name": "Exalted Lord (35 Destiny Pts / 300 pts)", "type": "upgrade", "costs": [{"name": "pts", "typeId": COST_PTS, "value": 300}]},
              ],
          },
          build_ptg_group(faction_name, anvil_name, is_hero=True),
      ],
  }
  shared_entries.append(anvil_entry)
  entry_links.append({"id": nr_id(f"el-anv-{faction_name}"), "name": anvil_name, "hidden": False, "type": "selectionEntry", "targetId": anvil_entry["id"]})

  return {
      "catalogue": {
          "id": nr_id(f"cat-file-{faction_name}"),
          "name": faction_name,
          "revision": 1,
          "battleScribeVersion": "2.03",
          "library": False,
          "gameSystemId": GS_ID,
          "gameSystemRevision": 2,
          "xmlns": "http://www.battlescribe.net/schema/catalogueSchema",
          "sharedSelectionEntries": shared_entries,
          "entryLinks": entry_links,
      }
  }


def main():
  gs_data = build_gamesystem()
  ensure_all_categories(gs_data)
  with open(GS_FILENAME, "w", encoding="utf-8") as gf:
    json.dump(gs_data, gf, indent=2)
  print(f"Compiled {GS_FILENAME} in root folder")

  for f_name, f_data in ALL_FACTIONS.items():
    cat_json = build_faction_catalogue(f_name, f_data)
    out_path = f"{f_name}.json"
    with open(out_path, "w", encoding="utf-8") as out_f:
      json.dump(cat_json, out_f, indent=2)
    print(f"  -> Compiled {out_path}")

  print(f"\nDone! Built {GS_FILENAME} + {len(ALL_FACTIONS)} faction catalogues in root folder.")


if __name__ == "__main__":
  main()