import sqlite3
from typing import List
from entities import Posting

DB_FILE = "inverted-index.db"


def clear_db():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM IndexWord")
        cur.execute("DELETE FROM Posting")


def create_postings(postings: List[Posting]):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        idxword_query = """INSERT OR IGNORE INTO IndexWord VALUES (?);"""
        cur.executemany(idxword_query, [(p.word,) for p in postings])
        posting_query = """INSERT INTO Posting VALUES (?, ?, ?, ?);"""
        cur.executemany(posting_query, [p.to_tuple() for p in postings])
        conn.commit()


def search(words):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        search_query = f"""SELECT p.documentName AS docName, 
                        SUM(frequency) AS freq, 
                        GROUP_CONCAT(indexes) AS idxs
                        FROM Posting p
                        WHERE p.word IN {tuple(words)}
                        GROUP BY p.documentName
                        ORDER BY freq DESC;"""

        cur.execute(search_query)
        result = cur.fetchmany(10)
        cur.close()
        return result