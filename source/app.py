import requests

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(500))

    def __repr__(self):
        return str(self.id)

    def show(self):
        return {'id': self.id,
                'userId': self.userId,
                'title': self.title,
                'body': self.body}

    def update(self, attr, value):
        if attr not in ["title", "body"]:
            return ('Wrong attribute. '
                    'Only title and/or body can be modified. Dropped.')
        if attr == "title":
            self.title = value
        if attr == "body":
            self.body = value
        db.session.add(self)
        db.session.commit()
        return 'Updated!'


class ExAPI():

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.baseurl = "https://jsonplaceholder.typicode.com/"

    def get_resource(self, id):
        url = self.baseurl + self.endpoint + str(id)
        try:
            resource = requests.get(url, verify=False,
                                    headers={"Content-Type":
                                             "application/json"})
            if resource:
                return resource
            return None
        except requests.exceptions.RequestException:
            return 1


def input_validation(request, action="add_post"):
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return {'msg': 'Invalid JSON request.'}, 400
        if request.content_length > 700:
            return {'msg': 'Request too long.'}, 422
        # title
        p_title = request_json['title']
        if not p_title or len(str(p_title)) > 80:
            return {'msg':
                    'Title value is missing or too long (max 80 chars).'}, 422
        # body
        p_body = request_json['body']
        if not p_body or len(str(p_body)) > 500:
            return {'msg':
                    'Body value is missing or too long (max 500 chars).'}, 422
        # userId
        if action == "add_post":
            p_userId = request_json['userId']
            if not p_userId or not str(p_userId).isdecimal():
                return {'msg': 'User ID is in wrong format or missing.'}, 422
    except KeyError as keymiss:
        if action == "add_post":
            return {'msg':
                    'Key {} is missing from request.'.format(keymiss)}, 422
    except (ValueError, AttributeError, TypeError):
        return {'msg': 'Wrong format of the request.'}, 400
    return request_json, 0


@app.get('/posts/<post_id>')
def get_post(post_id):
    try:
        post = Post.query.get(post_id)
        return post.show()
    except AttributeError:
        posts_ext_api = ExAPI("posts/")
        post_find = posts_ext_api.get_resource(post_id)
        if post_find == 1:
            return {'msg': 'Internal error.'}, 500
        if post_find:
            p = post_find.json()
            post = Post(id=p['id'],
                        userId=p['userId'],
                        title=p['title'],
                        body=p['body'])
            db.session.add(post)
            db.session.commit()
            return post.show(), 200

        return {'msg': 'Post not found.'}, 404


@app.get('/posts/from_user=<user_id>')
def get_user_posts(user_id):
    result = Post.query.filter(Post.userId == user_id)
    post_ids = result.all()
    posts = []
    for post_id in post_ids:
        post = Post.query.get(str(post_id))
        posts.append(post.show())
    if not posts:
        return {'msg': 'No posts from user {}'.format(user_id)}, 404
    return jsonify(posts)


@app.post('/posts')
def add_post():
    check = input_validation(request)
    if check[1] != 0:
        return check
    req = check[0]

    users_ext_api = ExAPI("users/")
    user_check = users_ext_api.get_resource(req['userId'])
    if not user_check:
        return {'msg': 'User not found.'}, 404
    if user_check == 1:
        return {'msg': 'Internal error.'}, 500

    post = Post(userId=req['userId'],
                title=req['title'],
                body=req['body'])
    db.session.add(post)
    db.session.commit()
    return post.show(), 201


@app.put('/posts/<post_id>')
def update_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404

    check = input_validation(request, "update_post")
    if check[1] != 0:
        return check
    req = check[0]

    result = {}
    code = 422
    for field in req.keys():
        value = req[field]
        update_action = post.update(field, value)
        result[field] = update_action
        if update_action == 'Updated!':
            code = 200

    return {"update_status": result, "post": post.show()}, code


@app.delete('/posts/<post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
    db.session.delete(post)
    db.session.commit()
    return {'msg': 'Post with ID {} deleted.'.format(post_id)}, 200
