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

## Database Set up (Windows)

Go to an empty folder and save the script into a subfolder named *init_scripts*. Create another empty folder named *pgdata*.

We run docker container using the following command. The command will name the container *postgresql-wier*, set username and password, map database files to folder *./pgdata* and initialization scripts to *./init-scripts*, map port 5432 to host machine (i.e. localhost) and run image *postgres:12.2* in a detached mode.

```
docker run --name postgresql-wier `
    -e POSTGRES_PASSWORD=SecretPassword `
    -e POSTGRES_USER=user `
    -v $PWD/pgdata:/var/lib/postgresql/data `
    -v $PWD/init-scripts:/docker-entrypoint-initdb.d `
    -p 5432:5432 `
    -d postgres:12.2
```

## How to run

Some instructions on how to run the crawler.
