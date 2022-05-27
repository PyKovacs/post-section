from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(300))

    def __repr__(self):
        return '{} : {}'.format(self.id, self.title)

@app.route('/')
def index():
    return 'Hey!'

@app.get('/posts/<post_id>')
def get_post(post_id):
    try:
        post = Post.query.get(post_id)
        return jsonify([{'userId' : post.userId}, 
                        {'title' : post.title},
                        {'body' : post.body}])
    except AttributeError:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
