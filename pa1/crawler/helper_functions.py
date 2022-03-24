import re
import os
import mimetypes
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

from urllib.parse import urlparse
from urllib.request import urlopen
import urllib.robotparser as urobot
from url_normalize import url_normalize
import requests
from entities import Image, PageData


def guess_type_of(link, strict=False):
    link_type, _ = mimetypes.guess_type(link)
    if link_type is None and strict:
        try:
            u = urlopen(link)
            link_type = u.info().get_content_type()
        except:
            pass
    return link_type


# def get_page(driver: WebDriver, url, type_code):
#     try:
#         print(f"Retrieving web page URL '{url}'")
#         driver.get(url)
#     except WebDriverException as e:
#         print(e)

#     if type_code == 'FRONTIER':
#         html_content = driver.page_source
#         images = get_all_images(driver, url)
#         links = get_all_links(driver, LIMIT_DOMAIN, ALLOWED_LINK_TYPES)
#         page_data = None
#     elif type_code == 'BINARY':
#         html_content, images, links = None, [], []
#         page_data = helper_functions.get_page_data(dest_url)
#     else:
#         html_content, images, links = None, [], []
#         page_data = None


def get_all_links(driver: WebDriver, limit_domain, allowed_link_types):
    links = []
    anchors = driver.find_elements_by_tag_name("a")
    for a in anchors:
        href = a.get_attribute("href")

        onclick = a.get_attribute("onclick")
        if onclick and ("location.href" in onclick or "document.location" in onclick):
            href = onclick.split("'")[-1]

        if type(href) != str:
            # print(f"href not string: '{href}'")
            continue

        o = urlparse(href)

        if not re.search(f"{limit_domain}$", str(o.hostname)):
            continue

        if o.scheme not in ["http", "https"]:
            continue

        link_type = guess_type_of(href)
        if link_type and link_type not in allowed_link_types:
            print(f"Not allowed link type: '{link_type}'")
            continue

        normalized_url = url_normalize(href)
        if normalized_url not in links:
            links.append(normalized_url)

    return links


def get_all_images(driver: WebDriver, page_url, store_binary):
    images = []
    imgs = driver.find_elements_by_tag_name("img")
    for img in imgs:

        src = img.get_attribute("src")
        o = urlparse(src)
        if o.scheme in ["http", "https"]:
            page = page_url
            filename = src.split("/")[-1]
            content_type = guess_type_of(src, strict=True)
            data = requests.get(src, verify=False).content if store_binary else None
            accessed_time = datetime.now()

            image = Image(page, filename, content_type, data, accessed_time)
            images.append(image)

    return images


def get_page_data(url, store_binary):
    data_type_code = url.split(".")[-1].upper()
    data = requests.get(url, verify=False).content if store_binary else None
    return PageData(url, data_type_code, data)


def get_robots_url(url):
    domain_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
    robots_url = domain_url + "/robots.txt"
    return robots_url


def parse_robots_file(url):
    robots_content, site_map_content = None, None
    robots_url = get_robots_url(url)

    rp = urobot.RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
        robots_content = urlopen(robots_url).read().decode("utf-8")
        site_maps = rp.site_maps()
        if site_maps:
            r = requests.get(site_maps[0])
            site_map_content = r.text
    except:
        print("Error: Parse Robots Failed!")

    return rp, robots_content, site_map_content
