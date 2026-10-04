import sqlite3

def get_db():
    conn = sqlite3.connect("recipe_platform.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            keywords TEXT,
            publication_date TEXT,
            chef_id INTEGER,
            labels TEXT,
            image_url TEXT,
            FOREIGN KEY(chef_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
