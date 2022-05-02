import sys
import os
import codecs
import glob
import regex
import json


def get_html(site_names):
    sites = []
    for site in site_names:
        path = r"../input-extraction/" + site + r"/*.html"
        files = glob.glob(path)
        pages = {}
        for f_path in files:
            f = codecs.open(f_path, "r", encoding="LATIN-1").read()
            f_name = f_path.split("/")[-1]
            pages[f_name] = str(f)

        sites.append(pages)

    return sites


def re_extract(sites):
    for site in sites:
        for p_name, p_html in site.items():
            print(f"\n {p_name}")

            title = regex.findall(r"<a.*<b>.*?<\/a>(?=<br>)", p_html)
            content = regex.findall(
                r'<span class="normal">.*?(?=<\/td>)', p_html, flags=regex.S
            )
            list_price = regex.findall(r"(?<=List Price:.*?)\$.*?(?=<)", p_html)
            price = regex.findall(r"(?<=>Price:.*?)\$.*?(?=<)", p_html)
            saving = regex.findall(r"(?<=You Save:.*?)\$.*?(?= )", p_html)
            saving_percent = regex.findall(r"(?<=You Save:.*?\$.*? ).*?(?=\<)", p_html)

            print(len(content))

            if not title:
                continue

            data_items = []
            for i in range(len(title)):
                dict = {
                    "Title": title[i],
                    "Content": content[i],
                    "ListPrice": list_price[i],
                    "Price": price[i],
                    "Saving": saving[i],
                    "SavingPercent": saving_percent[i],
                }
                data_items.append(dict)

                json_object = json.dumps(dict, indent=4)
                print(json_object)

    #     site["extracted"] = data_items

    # return sites


def xpath_extract(sites):
    pass


def auto_extract(sites):
    pass


if __name__ == "__main__":

    SITE_NAMES = ["overstock.com", "rtvslo.si"]

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