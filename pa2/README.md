# Programming assignment 2 (Data Extraction)
3 types of data extraction methods.

- (A) Data extraction using regular expressions only.
- (B) Data extraction using XPath only.
- (C) Generation of extraction rules using automatic Web extraction algorithm (RoadRunner).

## Installation

Move to the /pa2/implementation-extraction/ directory.
Create a new python virtual environment with conda and install requirements.
```
$ conda create --name <env> --file requirements.txt
```

## How to run

Run each of the implementations seperately with different arguments (A, B, C)

1. Regex Extraction
python run-extraction.py A

2. XPath Extraction
python run-extraction.py B

3. RoadRunner
python run-extraction.py C
