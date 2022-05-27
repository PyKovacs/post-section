from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '{} : {}'.format(self.id, self.title)

@app.route('/')
def index():
    return 'Hey!'

@app.get('/posts/<id>')
def get_post(id):
    post = Post.query.get(id)
    return {"title" : post.title}