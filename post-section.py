import os
from views import interface
from source.model import app, db


def main():
    app.register_blueprint(interface, url_prefix='/')

    #Initialize DB
    if not os.path.exists('./data/data.db'):
        os.mkdir("./data")
        db.create_all()

if __name__ == 'post-section':
    main()



'''
TO IMPROVE: 
- DB INIT ON START
- SWAGGER DOCU
- CODE STRUCTURE REVIEW
    - wrap app to class
- FRONTEND HTML,CSS
- PACKAGING
- README
- REVIEW TYPING
- MECHANISM FOR ID ASSIGN - assigning next, not first free
'''

'''
TODO:
- change show method in Post class to __str___
'''