# Programming assignment 3 (Data Processing, Indexing and Retrieval)
2 parts of the assignment.

- (1.) Data processing and indexing
- (2.) Data retrieval

## Installation

Move to the /pa3/implementation-indexing/ directory.
Create a new python virtual environment with conda and install requirements.
```
$ conda create --name <env> --file requirements.txt
```

## How to run

Files entities.py, preprocessing.py, stopwords.py, printer.py and repository.py contain helper functions.
The following scripts can be executed:

1. Create and populate the database (inverted-index.db)
```
python create-db.py
python populate-db.py
```

The following scripts execute the search and print results to stdin.
- (SEARCH_TERM) A string of characters inside "" for which to execute the search.
- (N_RESULTS) Number of results shown. Default = 10. (optional)
- (N_SNIPPETS) Number of snippets shown per result. Default = 3. (optional)

2. Run search queries **with** the use of database
```
python run-sqlite-search <SEARCH_TERM> <N_RESULTS> <N_SNIPPETS>
```

3. Run search queries **without** the use of database
```
python run-basic-search <SEARCH_TERM> <N_RESULTS> <N_SNIPPETS>
```

Search term examples:
- "predelovalne dejavnosti"
- "trgovina"
- "social services"
- "avtomobil"
- "cestno prometni predpisi"
- "preko zavoda za zaposlovanje"