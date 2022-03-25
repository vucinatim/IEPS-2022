# Programming assignment 1 (Crawler)
A standalone crawler that will crawl only .gov.si web sites. 
The crawler will roughly consist of the following components:

- HTTP downloader and renderer: To retrieve and render a web page.
- Data extractor: Minimal functionalities to extract images and hyperlinks.
- Duplicate detector: To detect already parsed pages.
- URL frontier: A list of URLs waiting to be parsed.
- Datastore: To store the data and additional metadata used by the crawler.

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

To run the crawler you must have the chromedriver executable inside the ./crawler directory.
Alternatively you can specify the location of your chromedriver executable manually in the *set up parameters* codeblock

You will also need to have a PostgreSQL database running and initialized with the provided schemas.
You can set the connection parameters in the *repository.py* file.

You can set multiple parameters of the crawler
```
LIMIT_DOMAIN = ".gov.si"
SEED_URLS = ["http://www.gov.si/", "http://www.evem.gov.si/", "http://e-uprava.gov.si/", "http://e-prostor.gov.si/"]
BINARY_CONTENT = ['pdf', 'doc', 'docx', 'ppt', 'pptx']
ALLOWED_LINK_TYPES = [
    'text/html', 
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

NUMBER_OF_WORKERS = 3
TIMEOUT = 5 # Default timeout if no robots.txt
START_CLEAN = False # If set to TRUE it will clear the database and start again from seed urls
STORE_BINARY = True # If set to TRUE it will store binary data of images and files
RESPECT_CRAWL_DELAY = True # If set to true the crawler will respect crawl_delay from robots.txt
```

To start the crawler run the *Start Crawler* codeblock.
