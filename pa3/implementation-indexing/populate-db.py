import glob
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from preprocessing import preprocess_text
from entities import Posting
import repository


SITE_NAMES = ["e-prostor.gov.si", "e-uprava.gov.si", "evem.gov.si", "podatki.gov.si"]

repository.clear_db()

for site in SITE_NAMES:
    path = r"../input-indexing/" + site + r"/*.html"
    files = glob.glob(path)
    for file in tqdm(files, desc=f"{site}"):
        with open(file, "r", encoding="utf-8") as html_page:
            soup = BeautifulSoup(html_page, "html.parser")
            html_text = soup.get_text()
            tokens, indexes = preprocess_text(html_text)

            postings = []
            unique_tokens = np.unique(tokens)
            for ut in unique_tokens:
                indices = np.where(tokens == ut)
                positions = indexes[indices]

                postings.append(Posting(file, ut, positions))

            repository.create_postings(postings)