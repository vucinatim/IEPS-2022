import regex
import json


def check_extraction(items, singles=0):
    new_items = list(items)
    for idx, i in enumerate(items):
        if not i:
            if idx < singles:
                new_items[idx] = ["! Error: could not extract !"]
            else:
                new_items[idx] = ["! Error: could not extract !"] * 50
    return tuple(new_items)


def clean(s):
    s = s.replace("\n", "")
    s = regex.sub(r"\t+", " ", s)
    s = regex.sub(r"^\s+|\s+$", "", s)
    return s


def print_overstock(items, name="overstock.com"):
    (
        title,
        content,
        list_price,
        price,
        saving,
        saving_percent,
    ) = check_extraction(items)

    object_list = []
    for i in range(len(title)):
        dict = {
            "Title": clean(title[i]),
            "Content": clean(content[i]),
            "ListPrice": clean(list_price[i]),
            "Price": clean(price[i]),
            "Saving": clean(saving[i]),
            "SavingPercent": clean(saving_percent[i]),
        }
        object_list.append(dict)

    json_list = json.dumps(object_list, indent=2, ensure_ascii=False)
    print(f"---- {name} ----")
    print(json_list + "\n")


def print_rtvslo(items, name="rtvslo.si"):
    (
        title,
        subtitle,
        lead,
        content,
        author,
        published_time,
    ) = check_extraction(items)

    object_list = []
    for i in range(len(title)):
        dict = {
            "Title": clean(title[i]),
            "SubTitle": clean(subtitle[i]),
            "Lead": clean(lead[i]),
            "Content": clean(content[i]),
            "Author": clean(author[i]),
            "PublishedTime": clean(published_time[i]),
        }
        object_list.append(dict)

    json_list = json.dumps(object_list, indent=2, ensure_ascii=False)
    print(f"---- {name} ----")
    print(json_list + "\n")


def print_ceneje(items, name="ceneje.si"):
    (
        title,
        top_price,
        top_disc_price,
        item_seller,
        item_price,
        item_disc_price,
    ) = check_extraction(items, singles=2)

    object_list = []
    for i in range(len(item_seller)):
        dict = {
            "Seller": clean(item_seller[i]),
            "Price": clean(item_price[i]),
            "Discount": clean(item_disc_price[i]),
        }
        object_list.append(dict)

    page_dict = {
        "Title": clean(title[0]),
        "TopPrice": clean(top_price[0]),
        "TopDiscount": clean(top_disc_price[0]),
        "Offers": object_list,
    }
    json_page = json.dumps(page_dict, indent=2, ensure_ascii=False)
    print(f"---- {name} ----")
    print(json_page + "\n")