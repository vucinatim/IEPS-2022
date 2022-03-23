import re
from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urlparse, urljoin, urlunsplit
from url_normalize import url_normalize
import requests
from entities import Image


def get_all_links(driver: WebDriver, limit_domain, banned_filetypes):
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

        if re.search(f"{banned_filetypes}$", str(href)):
            continue

        if o.scheme not in ["http", "https"]:
            continue

        links.append(url_normalize(href))

    return links


def get_all_images(driver: WebDriver):
    images = []
    imgs = driver.find_elements_by_tag_name("img")
    for img in imgs:

        src = img.get_attribute("src")
        o = urlparse(src)
        if o.scheme in ["http", "https"]:
            filename = src.split("/")[-1]
            content_type = img.get_attribute("content-type")
            data = requests.get(src, verify=False).content
            accessed_time = datetime.now()

            image = Image(filename, content_type, data, accessed_time)
            images.append(image)

    return images


def get_robots_data(driver: WebDriver, url, site_maps):
    robots_content = None
    sitemap_content = None

    driver.get(url)
    try:
        robots_content = driver.find_element_by_tag_name("pre").get_attribute(
            "textContent"
        )
    except NoSuchElementException:
        pass

    if site_maps:
        driver.get(site_maps[0])
        sitemap_content = driver.page_source

    return robots_content, sitemap_content


# Functions for possible use to store frontier on disk in
# order to not loose track of progress if an error occurs
def write_file(path, data):
    with open(path, "w") as file:
        if type(data) == list:
            for d in data:
                file.write(d)
        else:
            file.write(data)


def append_file(path, data):
    with open(path, "a") as file:
        if type(data) == list:
            for d in data:
                file.write(d + "\n")
        else:
            file.write(data + "\n")
