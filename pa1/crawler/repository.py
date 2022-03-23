import threading
import psycopg

from entities import Site, Page, Image, PageData

lock = threading.Lock()

DB_NAME = "crawldb"
DB_HOST = "localhost"
DB_USER = "user"
DB_PASSWORD = "SecretPassword"


def clear_db():
    with psycopg.connect(
        dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD
    ) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM data_type, image, link, page, page_data, site")


def create_site(site: Site):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO site (domain, robots_content, sitemap_content) VALUES (%s, %s, %s)",
                    site.to_tuple(),
                )
