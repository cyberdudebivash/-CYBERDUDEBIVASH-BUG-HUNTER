import sqlite3

DB = "assets.db"


def init():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets(
        domain TEXT,
        host TEXT,
        ip TEXT,
        technologies TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_asset(domain, host, ip, tech):

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO assets VALUES(?,?,?,?)",
        (domain, host, str(ip), ",".join(tech) if tech else "")
    )

    conn.commit()
    conn.close()


init()