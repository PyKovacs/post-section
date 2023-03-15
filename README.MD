# Post_section

Post section provides API interface to post, fetch, update and delete posts.
External API https://jsonplaceholder.typicode.com is used to validate the user when posting, and to retrieve any posts not found in local db.

## Installation

1. Extract tarball package:
```
tar -xvzf post_section-package-0.1.tar.gz
```

2. *(Optional)* Create and activate python virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install PIP dependencies listed in [requirements.txt](requirements.txt):
```
pip3 install -r requirements.txt 
```

## First run

1. Initiate the db (don't mind the warning message):
```python3 source/db_init.py```

2. Start flask:
```flask run```

3. Bon APItite :)
