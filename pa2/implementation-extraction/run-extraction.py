import sys
import codecs
import glob
import re

from A import re_extract
from B import xpath_extract
from C import auto_extract


def get_html(site_names):
    sites = []
    for site in site_names:
        path = r"../input-extraction/" + site + r"/*.html"
        files = glob.glob(path)
        pages = {}
        for f_path in files:
            with codecs.open(f_path, "r", encoding="utf-8", errors="ignore") as f:
                f_name = f_path.split("/")[-1]
                pages[f_name] = re.sub(" +", " ", str(f.read()))

        sites.append(pages)

    return sites


# -*- coding: UTF-8 -*-

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")

    SITE_NAMES = ["overstock.com", "rtvslo.si", "ceneje.si"]

    if len(sys.argv) < 2:
        print("Error: no arguments passed.")
        exit()

    algo_type = sys.argv[1]

    if algo_type not in ["A", "B", "C"]:
        print(f"Error: argument '{algo_type}' is unknown. Use arguments A, B, or C.")
        exit()

    sites = get_html(SITE_NAMES)

    if algo_type == "A":
        re_extract(sites)
    elif algo_type == "B":
        xpath_extract(sites)
    elif algo_type == "C":
        auto_extract(sites)