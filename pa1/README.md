# Programming assignment 1 (Crawler)
- HTTP downloader and renderer: To retrieve and render a web page.
- Data extractor: Minimal functionalities to extract images and hyperlinks.
- Duplicate detector: To detect already parsed pages.
- URL frontier: A list of URLs waiting to be parsed.
- Datastore: To store the data and additional metadata used by the crawler.

## TO-DO

> * DB interface (with methods in existing entities classes).
> * Parallelization with threads and locking.
> * Duplication checks by comparing pages from DB.
> * Canonicalization of stored urls.
> * Robots.txt content extraction improvement in get_robots_data().
> * Squashing bugs.

## Installation

Create a new python virtual environment with conda and install requirements.
```
$ conda create --name <env> --file requirements.txt
```
Then download chromedriver from https://chromedriver.chromium.org/ for selenium web scraper and put it inside ./crawler directory.

## Set up

Some setup instructions.

## How to run

Some instructions on how to run the crawler.
