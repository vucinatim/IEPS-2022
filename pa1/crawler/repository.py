from typing import List
import threading
import psycopg
import mmh3

from entities import Site, Page, Image, PageData, Link, FrontierEntry, Error

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
                    "TRUNCATE crawldb.image, crawldb.link, crawldb.page, crawldb.page_data, crawldb.site, crawldb.frontier"
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
                    "INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time, html_content_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        site_id,
                        *page.to_tuple(),
                        mmh3.hash(page.html_content) if page.html_content else None,
                    ),
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
    if link.from_page is None or link.to_page is None:
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


def get_all_links():
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute("SELECT from_page, to_page FROM crawldb.link")
                return cur.fetchall()


def check_if_duplicate(html_content):
    if not html_content:
        return None
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT url FROM crawldb.page WHERE html_content_hash = %s",
                    (mmh3.hash(html_content),),
                )
                q = cur.fetchone()
                return q[0] if q is not None else None


def create_frontier_entries(frontier_entries: List[FrontierEntry]):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO crawldb.frontier (src_url, dest_url, crawled, fetched, processed) VALUES (%s, %s, %s, %s, %s)",
                    [f.to_tuple() for f in frontier_entries],
                )


def get_next_frontier_entry():
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT (id, src_url, dest_url) FROM crawldb.frontier WHERE fetched = %s ORDER BY id LIMIT 1",
                    (False,),
                )
                q = cur.fetchone()
                if q is not None:
                    cur.execute(
                        "UPDATE crawldb.frontier SET fetched = %s WHERE id = %s",
                        (True, q[0][0]),
                    )
                    return q[0]
                else:
                    return None


# def get_next_frontier_entry():
#     with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
#         conn.autocommit = True
#         with lock:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT (id, src_url, dest_url) FROM crawldb.frontier WHERE fetched = %s AND new_site=true ORDER BY id LIMIT 1",
#                     (False,),
#                 )
#                 q = cur.fetchone()
#                 if q is not None:
#                     cur.execute(
#                         "UPDATE crawldb.frontier SET fetched = %s WHERE id = %s",
#                         (True, q[0][0]),
#                     )
#                     return q[0]
#                 else:
#                     return None


# def get_next_frontier_entry():
#     with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
#         conn.autocommit = True
#         with lock:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT (id, src_url, dest_url) FROM crawldb.frontier WHERE fetched = %s AND dest_url NOT IN (SELECT url FROM crawldb.page) ORDER BY id LIMIT 1",
#                     (False,),
#                 )
#                 q = cur.fetchone()
#                 if q is not None:
#                     cur.execute(
#                         "UPDATE crawldb.frontier SET fetched = %s WHERE id = %s",
#                         (True, q[0][0]),
#                     )
#                     return q[0]
#                 else:
#                     return None


def update_frontier_entry_to_crawled(id):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE crawldb.frontier SET crawled = %s WHERE id = %s", (True, id)
                )


def update_frontier_entry_to_processed(id):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE crawldb.frontier SET processed = %s WHERE id = %s",
                    (True, id),
                )


def create_error(error: Error):
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO crawldb.error (url, message, error_time) VALUES (%s, %s, %s)",
                    error.to_tuple(),
                )


# DB Managing Functions
def update_html_content_hashes():
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, html_content FROM crawldb.page WHERE html_content IS NOT NULL"
                )
                rows = cur.fetchall()
                hashes = [(id, mmh3.hash(html_content)) for (id, html_content) in rows]
                update_query = """UPDATE crawldb.page AS p
                     SET html_content_hash = e.hash 
                     FROM (VALUES (%s, %s)) AS e(id, hash) 
                     WHERE e.id = p.id;"""

                cur.executemany(update_query, hashes)


def update_new_sites():
    with psycopg.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD) as conn:
        conn.autocommit = True
        with lock:
            with conn.cursor() as cur:
                cur.execute("SELECT url FROM crawldb.page")
                page_rows = set(cur.fetchall())
                print("Page rows fetched")
                cur.execute("SELECT id, dest_url FROM crawldb.frontier")
                frontier_rows = cur.fetchall()
                print("Frontier rows fetched")
                new_urls = [
                    (f_id, f_url)
                    for f_id, f_url in frontier_rows
                    if (f_url,) not in page_rows
                ]
                print(f"New urls: {len(new_urls)}")
                update_query = """UPDATE crawldb.frontier AS p
                     SET new_site = true
                     FROM (VALUES (%s, %s)) AS e(id, url)
                     WHERE e.id = p.id;"""

                cur.executemany(update_query, new_urls[:60000])
