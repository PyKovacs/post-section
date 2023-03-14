import os

from source import app, db
from source.api import api_interface


def main() -> None:
    #Initialize DB
    if not os.path.exists('./data/data.db'):
        os.mkdir("./data")
        db.create_all()

    app.register_blueprint(api_interface, url_prefix='/api')

if __name__ == 'app':
    main()



'''
TO IMPROVE: 
DONE - DB INIT ON START
DONE - SWAGGER DOCU
DONE - CODE STRUCTURE REVIEW
- FRONTEND HTML,CSS
- PACKAGING
- README
DONE - REVIEW TYPING
'''