import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

conn = sqlite3.connect(DATA_DIR / 'loot.db')

cursor = conn.cursor()

cursor.executescript('''
    CREATE TABLE IF NOT EXISTS mobs (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        level INTEGER,
        classification TEXT
    );

    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quality TEXT
    );

    CREATE TABLE IF NOT EXISTS loot_table (
        mob_id INTEGER REFERENCES mobs(id),
        item_id INTEGER REFERENCES items(id),
        drop_chance REAL,
        min_quantity  INTEGER DEFAULT 1,
        max_quantity  INTEGER DEFAULT 1,
        PRIMARY KEY (mob_id, item_id)
    );
    
    CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE IF NOT EXISTS item_stats (
        item_id INTEGER REFERENCES items(id),
        stat_id INTEGER REFERENCES stats(id),
        value INTEGER
    )

''')

icc_bosses = [
    (36612,"Lord Marrowgar", 83,"boss"),
    (36855,"Lady Deathwhisper", 83,"boss"),
    (37813,"Deathbringer Saurfang", 83,"boss"),
    (36626,"Festergut", 83,"boss"),
    (36627,"Rotface", 83,"boss"),
    (36678,"Professor Putricide", 83,"boss"),
    (37970,"Prince Valanar", 83,"boss"),
    (37955,"Blood-Queen Lana'thel", 83,"boss"),
    (36789,"Valithria Dreamwalker", 83,"boss"),
    (36853,"Sindragosa <Queen of the Frostbrood>", 83,"boss"),
    (36597,"The Lich King", 83,"boss")
]

cursor.executemany("INSERT OR IGNORE INTO mobs (id, name, level, classification) VALUES (?, ?, ?, ?)", icc_bosses)

def load_items_csv(path):
    items = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = int(row["id"])
            items.append((item_id, row["name"], row["quality"]))

    return items

icc_boss_items = load_items_csv(DATA_DIR / 'icc_items.csv')

cursor.executemany("INSERT OR IGNORE INTO items (id, name, quality) VALUES (?, ?, ?)", icc_boss_items)

def load_loot_csv(path):
    loot = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mob_id = int(row["mob_id"])
            item_id = int(row["item_id"])
            drop_chance = float(row["drop_chance"]) / 100
            min_q = int(row["min_quantity"] or 1)
            max_q = int(row["max_quantity"] or 1)

            loot.append((mob_id,item_id,drop_chance,min_q,max_q))

    return loot

icc_loot_table = load_loot_csv(DATA_DIR / 'icc_loot_table.csv')

cursor.executemany("INSERT OR IGNORE INTO loot_table (mob_id, item_id, drop_chance, min_quantity, max_quantity) VALUES (?, ?, ?, ?, ?)", icc_loot_table)

conn.commit()


## TEST ##
# cursor.execute("SELECT COUNT(*) FROM loot_table")
# print(cursor.fetchone()[0])

# cursor.execute("SELECT item_id FROM loot_table WHERE item_id NOT IN (SELECT id FROM items)")
# print(cursor.fetchall())