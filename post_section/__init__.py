from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

import post_section.source.views
db.create_all()

'''
TO IMPROVE: 
DONE - DB INIT ON START
DONE - SWAGGER DOCU
DONE - CODE STRUCTURE REVIEW
- PACKAGING
- README
DONE - REVIEW TYPING
'''