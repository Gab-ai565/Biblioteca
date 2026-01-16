import sqlite3

def init_db():
    conn = sqlite3.connect("biblioteca.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano INTEGER NOT NULL,
        estado BOOLEAN NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
