import sqlite3


def startup():
    conn = sqlite3.connect('../db.sqlite3')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS slots(
                slotid INTEGER PRIMARY KEY,
                starttime TEXT,
                endtime   TEXT
              )''')
    c.execute('''CREATE TABLE IF NOT EXISTS rooms(
                room TEXT,
                date TEXT,
                slotid INTEGER,
                FOREIGN KEY(slotid) REFERENCES slots(slotid)
              )''')

    conn.commit()
    conn.close()
