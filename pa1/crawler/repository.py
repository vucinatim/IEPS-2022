from typing import List
import threading
import psycopg

from entities import Site, Page, Image, PageData, Link

lock = threading.Lock()

DB_NAME = "user"
DB_HOST = "localhost"
DB_USER = "user"
DB_PASSWORD = "SecretPassword"


def clear_db():
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "TRUNCATE crawldb.image, crawldb.link, crawldb.page, crawldb.page_data, crawldb.site"
                )


def create_site(site: Site):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO crawldb.site (domain, robots_content, sitemap_content) VALUES (%s, %s, %s)",
                    site.to_tuple(),
                )


def check_if_site_exists(domain):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM crawldb.site WHERE domain = %s", (domain,))
                return cur.fetchone() is not None


def create_page(page: Page):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawldb.site WHERE domain = %s", (page.site,)
                )
                site_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (site_id, *page.to_tuple()),
                )


def check_if_page_exists(url):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM crawldb.page WHERE url = %s", (url,))
                return cur.fetchone() is not None


def create_images(images: List[Image]):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawldb.page WHERE url = %s", (images[0].page,)
                )
                page_id = cur.fetchone()[0]
                cur.executemany(
                    "INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time) VALUES (%s, %s, %s, %s, %s)",
                    [(page_id, *i.to_tuple()) for i in images],
                )


def create_page_data(page_data: PageData):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawldb.page WHERE url = %s", (page_data.page,)
                )
                page_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO crawldb.page_data (page_id, data_type_code, data) VALUES (%s, %s, %s)",
                    (page_id, *page_data.to_tuple()),
                )


def create_link(link: Link):
    if not link.from_page or not link.to_page:
        return
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawldb.page WHERE url = %s", (link.from_page,)
                )
                from_page_id = cur.fetchone()[0]
                cur.execute(
                    "SELECT id FROM crawldb.page WHERE url = %s", (link.to_page,)
                )
                to_page_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO crawldb.link (from_page, to_page) VALUES (%s, %s)",
                    (from_page_id, to_page_id),
                )


def check_if_duplicate(html_content):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT url FROM crawldb.page WHERE html_content = %s",
                    (html_content,),
                )
                q = cur.fetchone()
                return q[0] if q is not None else None