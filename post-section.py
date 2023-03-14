import os

from source.model import app, db
from api import api_interface


def main() -> None:
    #Initialize DB
    if not os.path.exists('./data/data.db'):
        os.mkdir("./data")
        db.create_all()

    app.register_blueprint(api_interface, url_prefix='/api')

if __name__ == 'post-section':
    main()



'''
TO IMPROVE: 
DONE - DB INIT ON START
- SWAGGER DOCU
- CODE STRUCTURE REVIEW
    - wrap app to class
- FRONTEND HTML,CSS
- PACKAGING
- README
- REVIEW TYPING
'''