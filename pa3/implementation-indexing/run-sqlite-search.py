# -*- coding: UTF-8 -*-
import sys
import time
import repository
from preprocessing import preprocess_text
from printer import print_results

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Error: no arguments passed.")
        exit()

    n_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    n_snippets = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    search_term = sys.argv[1]
    search_words, _ = preprocess_text(search_term)

    start = time.perf_counter()
    results = repository.search(search_words)
    stop = time.perf_counter()

    dt = round((stop - start) * 1000)

    print_results(results, search_term, dt, n_results=n_results, n_snippets=n_snippets)
