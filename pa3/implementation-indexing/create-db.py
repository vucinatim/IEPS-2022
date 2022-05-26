import sqlite3

conn = sqlite3.connect("inverted-index.db")

c = conn.cursor()

c.execute(
    """
    CREATE TABLE IndexWord (
        word TEXT PRIMARY KEY
    );
"""
)

c.execute(
    """
    CREATE TABLE Posting (
        word TEXT NOT NULL,
        documentName TEXT NOT NULL,
        frequency INTEGER NOT NULL,
        indexes TEXT NOT NULL,
        PRIMARY KEY(word, documentName),
        FOREIGN KEY (word) REFERENCES IndexWord(word)
    );
"""
)

conn.commit()
conn.close()
