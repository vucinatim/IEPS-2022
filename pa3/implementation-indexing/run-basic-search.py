# -*- coding: UTF-8 -*-
import sys
import time
import glob
from tqdm import tqdm
from bs4 import BeautifulSoup
from preprocessing import preprocess_text
from printer import print_results

SITE_NAMES = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]


def basic_search(search_words):
    results = []
    for site in SITE_NAMES:
        path = r"../input-indexing/" + site + r"/*.html"
        files = glob.glob(path)
        for file in tqdm(files, desc=f"{site}"):
            with open(file, "r", encoding="utf-8") as html_page:
                soup = BeautifulSoup(html_page, "html.parser")
                html_text = soup.get_text()
                tokens, indexes = preprocess_text(html_text)

                found_indexes = []
                for idx, t in zip(indexes, tokens):
                    if t in search_words:
                        found_indexes.append(str(idx))

                if found_indexes:
                    document_name = file.split("/")[-1].replace("\\", "/")
                    results.append(
                        [document_name, len(found_indexes), ",".join(found_indexes)]
                    )

    return sorted(results, key=lambda item: item[1], reverse=True)[:10]


if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Error: no arguments passed.")
        exit()

    search_term = sys.argv[1]
    search_words, _ = preprocess_text(search_term)

    start = time.perf_counter()
    results = basic_search(search_words)
    stop = time.perf_counter()

    dt = round((stop - start) * 1000)

    print_results(results, search_term, dt)
