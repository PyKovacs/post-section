# Post-Section

Post section provides API interface to post, display, update and delete posts.
External API https://jsonplaceholder.typicode.com is used to validate the user when posting, and to retrieve any posts not found in local db.

## Installation

Unpack post-section-package-0.1.tar.gz and install PIP dependecies listed in [requirements.txt](requirements.txt):
```
pip3 install -r requirements.txt 
```

## First run

Navigate to source/ folder and:
1. Initiate the db:
```python3 db_init.py```

2. Start flask:
```flask run```
