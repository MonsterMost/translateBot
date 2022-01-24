import sqlite3 as sql

db = sql.connect('tgtrdif.db', check_same_thread=False)

cursor = db.cursor()


cursor.executescript('''
DROP TABLE IF EXISTS history;
CREATE TABLE IF NOT EXISTS history(
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT,
    firstLast  TEXT,
    username TEXT,
    messagetext TEXT,
    traslatetext TEXT,
    definition TEXT,
    messagetime TEXT 
);
''')

db.commit()
db.close()
