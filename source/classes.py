import requests
from flask import Flask
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
        '''Returns only ID, for db operations.'''
        return str(self.id)

    def show(self):
        '''Returns human readable represantation.'''
        return {'id': self.id,
                'userId': self.userId,
                'title': self.title,
                'body': self.body}

    def update(self, attr: str, value: str):
        '''Checks the update request and updates the post, commiting to db.'''
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

    @staticmethod
    def input_validation(request, action: str = 'add_post'):
        try:
            # whole request body
            request_json = request.get_json(silent=True)
            if not request_json:
                return {'msg': 'Invalid JSON request.'}, 400
            if request.content_length > 700:
                return {'msg': 'Request too long.'}, 422

            # title
            p_title = request_json['title']
            if not p_title or len(str(p_title)) > 80:
                return {'msg':
                        'Title value is missing or '
                        'too long (max 80 chars).'}, 422
            # body
            p_body = request_json['body']
            if not p_body or len(str(p_body)) > 500:
                return {'msg':
                        'Body value is missing or '
                        'too long (max 500 chars).'}, 422
            # userId
            if action == 'add_post':
                p_userId = request_json['userId']
                if not p_userId or not str(p_userId).isdecimal():
                    return {'msg': 'User ID is in '
                            'wrong format or missing.'}, 422

        except KeyError as keymiss:
            if action == 'add_post':
                return {'msg':
                        'Key {} is missing from request.'.format(keymiss)}, 422
        except (ValueError, AttributeError, TypeError):
            return {'msg': 'Wrong format of the request.'}, 400
        return request_json, 0


class ExAPI:
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.baseurl = 'https://jsonplaceholder.typicode.com/'

    def get_resource(self, id: int):
        url = self.baseurl + self.endpoint + str(id)
        try:
            resource = requests.get(url, verify=False,
                                    headers={'Content-Type':
                                             'application/json'})
            if resource:
                return resource
            return None
        except requests.exceptions.RequestException:
            return 1
