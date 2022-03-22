from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from entities import Site, Page, Image
import requests
from selenium.common.exceptions import NoSuchElementException


def get_all_links(driver: WebDriver):
    links = []
    anchors = driver.find_elements_by_tag_name("a")
    for a in anchors:
        href = a.get_attribute("href")
        if href != "" and href != None:
            links.append(href)

    return links


def get_all_images(driver: WebDriver):
    images = []
    imgs = driver.find_elements_by_tag_name("img")
    for img in imgs:

        src = img.get_attribute("src")
        o = urlparse(src)
        if o.scheme != "http" and o.scheme != "https":
            continue
        filename = src.split("/")[-1]
        content_type = img.get_attribute("content-type")
        data = requests.get(src).content
        accessed_time = datetime.now().time()

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
