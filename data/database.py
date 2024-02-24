import sqlite3


def initialize_db():
    conn = sqlite3.connect("sqlite3.db")

    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists players(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE)""")
    c.execute("""CREATE TABLE if not exists chessgames(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player INTEGER,
            opponent TEXT,
            player_side TEXT,
            result TEXT,
            moves_count INTEGER,
            date TEXT,
            FOREIGN KEY(player) REFERENCES players(id))""")
    conn.commit()
    conn.close()


def insert_data(query, values=()):
    conn = sqlite3.connect("sqlite3.db")

    c = conn.cursor()
    c.execute(query, values)
    conn.commit()
    conn.close()


def show_data(query, values=()):
    conn = sqlite3.connect("sqlite3.db")
    c = conn.cursor()
    c.execute(query, values)
    records = c.fetchall()
    conn.commit()
    conn.close()

    return records


def wipe_data():
    conn = sqlite3.connect("sqlite3.db")
    c = conn.cursor()
    c.execute("DELETE FROM chessgames")
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()

