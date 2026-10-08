# WoW Loot Sim

A Python project that simulates World of Warcraft raid loot drops. Pick a boss, kill it, and roll on its loot table using real drop rates.

> Work in progress: the database is built but the loot roll and menu are next. Also the stats are not attached to items yet / in the data base schema.

## Data

Loot tables cover the 11 bosses of **Icecrown Citadel (Heroic 25)**, with drop rates from [Wowhead](https://www.wowhead.com/mop-classic/zone=4812/icecrown-citadel).

Wrath of the Lich King Classic is no longer live, so the data comes from **Mists of Pandaria Classic**, the closest current version with ICC. Because ICC is legacy content there, rates mostly reflect max-level players farming the raid and may differ slightly from original Wrath (unforch but still fun for me).

## Getting started

Requires Python 3. No external packages; it uses only standard libraries (`sqlite3`, `csv`, `pathlib`).

```
git clone https://github.com/Sam-McNe/WoW_loot_sim.git
cd WoW_loot_sim
python db.py
```

`db.py` builds `data/loot.db` from the CSV files. The database itself isn't tracked in git, so it's rebuilt from source data.

## Project structure

```
WoW_loot_sim/
├── db.py          # creates tables and loads data from CSVs
├── loot.py        # loot roll logic (in progress)
├── main.py        # boss selection menu (in progress)
└── data/
    ├── icc_items.csv
    └── icc_loot_table.csv
```

## Database schema

| Table        | Purpose                                                         |
|--------------|-----------------------------------------------------------------|
| `mobs`       | Bosses: NPC ID, name, level, classification                     |
| `items`      | Items: item ID, name, quality                                   |
| `loot_table` | Links bosses to items with drop chance and quantity range       |
| `stats`      | Stat names (Strength, Haste, etc.)                              |
| `item_stats` | Links items to their stats and values                           |

IDs match in-game NPC and item IDs, so any row can be looked up on Wowhead. Drop chance lives on `loot_table` rather than `items`, because the same item can drop from multiple bosses at different rates. 