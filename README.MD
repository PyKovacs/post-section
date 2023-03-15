# Post_section

Post section provides API interface to post, fetch, update and delete posts.
External API https://jsonplaceholder.typicode.com is used to validate the user when posting, and to retrieve any posts not found in local db.

*NOTE: As this code is not considered for production environment, flask is only running dev server on local host, **therefore it is not accessible from outside.***

## Installation

1. Create and activate python virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install post-section wheel package located in *dist* folder:
```
pip3 install dist/post_section-0.0.10-py3-none-any.whl
```

## First run

1. Start flask with app parameter *post_section*:
```
flask --app post_section run
```

2. Bon APItite :)
