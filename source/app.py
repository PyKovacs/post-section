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

    def show(self):
        return {'id' : self.id,
                'userId' : self.userId, 
                'title' : self.title,
                'body' : self.body}

    def update(self, attr, value):
        if attr not in ["title", "body"]:
            return 'Wrong attribute. Only title and/or body can be modified. Dropped.'
        if not value:
            return 'Invalid value. Dropped.'
        if attr == "title":
            if len(str(value)) > 80:
                return 'Title too long (max 80 characters). Dropped.'
            self.title = value
        if attr == "body":
            if len(str(value)) > 300:
                return 'Body too long (max 300 characters). Dropped.'
            self.body = value
        db.session.add(self)
        db.session.commit()  
        return 'Updated!'

@app.get('/posts/<post_id>')
def get_post(post_id):
    try:
        post = Post.query.get(post_id)
        return post.show()
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
    ### input validation
    try:
        # userid
        p_userid = request.json['userId']
        if not p_userid or not str(p_userid).isdecimal():
            return {'msg': 'User ID is in wrong format or missing.'}, 400
        # title
        p_title = request.json['title']
        if not p_title or len(str(p_title)) > 80:
            return {'msg': 'Title is missing or too long (max 80 chars).'}, 400
        # body
        p_body = request.json['body']
        if not p_body or len(str(p_body)) > 300:
            return {'msg': 'Body is missing or too long (max 300 chars).'}, 400
    except (ValueError, AttributeError, TypeError):
        return {'msg': 'Wrong format of the request.'}, 400
    
    post = Post(userId=p_userid,
                title=p_title,
                body=p_body)
    db.session.add(post)
    db.session.commit()
    return post.show(), 201

@app.put('/posts/<post_id>')
def update_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404

    result = {}
    code = 422
    for field in request.json.keys():
        value = request.json[field]
        update_action = post.update(field, value)
        result[field] = update_action
        if update_action == 'Updated!':         
            code = 200
  
    return {"update_status" : result, "post" : post.show()}, code

@app.delete('/posts/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
    db.session.delete(post)
    db.session.commit()
    return {'msg': 'Post with ID {} deleted.'.format(post_id)}, 200
        