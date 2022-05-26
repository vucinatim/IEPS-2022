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

    search_term = sys.argv[1]
    search_words, _ = preprocess_text(search_term)

    start = time.perf_counter()
    results = repository.search(search_words)
    stop = time.perf_counter()

    dt = round((stop - start) * 1000)

    print_results(results, search_term, dt)
