from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from source.utils import call_external_api, validate_input

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    userId: int = db.Column(db.Integer)
    title: str = db.Column(db.String(80), nullable=False)
    body: str = db.Column(db.String(500))

    def __repr__(self) -> str:
        '''Returns ID as string, for db operations.'''
        return str(self.id)

    def show(self) -> dict[str, (int|str)] :
        '''Returns human readable representation.'''
        return {'id': self.id,
                'userId': self.userId,
                'title': self.title,
                'body': self.body}
    
    def update(self, attr: str, value: str) -> str:
        '''Checks the update request and updates the post, commit to db.'''
        if attr not in ['title', 'body']:
            return ('Wrong attribute. Only title '
                    'and/or body can be modified. Dropped.')
        if attr == 'title':
            self.title = value
        if attr == 'body':
            self.body = value
        db.session.add(self)
        db.session.commit()
        return 'Updated!'
    
    @classmethod
    def get(cls, post_id):
        '''
        Performs GET request with post ID as parameter.
        Example url: http://127.0.0.1:5000/posts/104

        If post not found, search for post on external API.
        '''
        try:
            post = cls.query.get(post_id)
            return post.show()
        except AttributeError:
            post_find = call_external_api('posts/', post_id)
            if post_find:
                p = post_find.json()
                post = cls(id=p['id'],
                            userId=p['userId'],
                            title=p['title'],
                            body=p['body'])
                db.session.add(post)
                db.session.commit()
                return post.show(), 200
            return {'msg': 'Post not found.'}, 404

    @classmethod
    def user_get(cls, user_id):
        '''
        Performs GET request with user ID as parameter.
        Example url: http://127.0.0.1:5000/posts/from_user=9
        '''
        result = cls.query.filter(cls.userId == user_id)
        post_ids = result.all()
        posts = []
        for post_id in post_ids:
            post = cls.query.get(str(post_id))
            posts.append(post.show())
        if not posts:
            return {'msg': 'No posts from user {}'.format(user_id)}, 404
        return jsonify(posts)

    @classmethod
    def add(cls):
        '''
        Performs POST request. Request must contain data.
        Example url: http://127.0.0.1:5000/posts

        User ID is validated against external API.
        '''
        check = validate_input(request)
        if check[1] != 0:
            return check
        req = check[0]

        # user validation on external API
        user_check = call_external_api('users/', req['userId'])
        if not user_check:
            return {'msg': 'User not found.'}, 404
        if user_check == 1:
            return {'msg': 'Internal error.'}, 500

        post = cls(userId=req['userId'],
                    title=req['title'],
                    body=req['body'])
        db.session.add(post)
        db.session.commit()
        return post.show(), 201

    @classmethod
    def update_post(cls, post_id):
        '''
        Performs PUT request with post ID as parameter.
        Request must contain data.
        Example url: http://127.0.0.1:5000/posts/104
        '''

        # find post
        post = cls.query.get(post_id)
        if post is None:
            return {'msg': 'Post ID {} not found.'.format(post_id)}, 404

        # data validation
        check = validate_input(request, 'update_post')
        if check[1] != 0:
            return check
        req = check[0]

        # update
        result = {}
        code = 422
        for field, value in req.items():
            update_action = post.update(field, value)
            result[field] = update_action
            if update_action == 'Updated!':
                code = 200

        return {'update_status': result, 'post': post.show()}, code

    @classmethod
    def delete(cls, post_id):
        '''
        Performs DELETE request with post ID as parameter.
        Example url: http://127.0.0.1:5000/posts/104
        '''
        post = cls.query.get(post_id)
        if post is None:
            return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
        db.session.delete(post)
        db.session.commit()
        return {'msg': 'Post with ID {} deleted.'.format(post_id)}, 200




