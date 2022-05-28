from ast import stmt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
#import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(300))

    def __repr__(self):
        return str(self.id)

@app.route('/')
def index():
    return 'Hey!'

@app.get('/posts/<post_id>')
def get_post(post_id):
    try:
        post = Post.query.get(post_id)
        return {'id' : post.id,
                'userId' : post.userId, 
                'title' : post.title,
                'body' : post.body}
    except AttributeError:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404

@app.get('/posts/from_user=<user_id>')
def get_user_posts(user_id):
    result = Post.query.filter(Post.userId == user_id)
    post_ids = result.all()
    posts = []
    for post_id in post_ids:
        post = Post.query.get(str(post_id))
        posts.append({'id' : post.id,
                      'userId' : post.userId, 
                      'title' : post.title,
                      'body' : post.body})
    return jsonify(posts)

@app.post('/posts')
def add_post():
    post = Post(userId=request.json['userId'],
                title=request.json['title'],
                body=request.json['body'])
    db.session.add(post)
    db.session.commit()
    return {'id' : post.id,
            'userId' : post.userId, 
            'title' : post.title,
            'body' : post.body}, 201

@app.delete('/posts/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post == None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
    db.session.delete(post)
    db.session.commit()
    return {'msg': 'Post with ID {} deleted.'.format(post_id)}, 200
        