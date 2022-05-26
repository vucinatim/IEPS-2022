from tabulate import tabulate
from colorama import Fore
import os
from bs4 import BeautifulSoup

PATH = r"../input-indexing/"


def print_results(results, query, time, n_results=10, n_snippets=3):
    # print("Results for a query: " + Fore.BLUE + '"' + query + '"' + Fore.WHITE + "\n\n")
    print("Results for a query: " + '"' + query + '"' + "\n\n")
    print(f"Results found in {time}ms.")
    print(f"Showing top {n_results} results limited to {n_snippets} snippets.\n\n")
    data = []
    for row in results[:n_results]:
        snippets = ""
        file = os.path.join(PATH, row[0])
        with open(file, "r", encoding="utf-8") as html_page:
            soup = BeautifulSoup(html_page, "html.parser")
            html_text = soup.get_text().split()
            indexes = row[2].split(",")[:n_snippets]
            for idx in indexes:
                start = max(0, int(idx) - 2)
                stop = min(len(html_text) - 1, int(idx) + 3)
                snippet = " ".join(html_text[start:stop])
                snippets += f"{'... ' if start > 0 else ''}{snippet}{' ... ' if stop < len(html_text) - 1 else ' '}"

        data.append([row[1], row[0], snippets])

    print(tabulate(data, headers=["Frequencies ", "Document", "Snippet"]))
