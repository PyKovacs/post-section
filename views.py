from flask import Blueprint

from source.model import Post

interface = Blueprint(__name__, 'interface')
post_model = Post()

@interface.get('/posts/<post_id>')
def get_post(post_id):
    return Post.get(post_id)

@interface.get('/posts/from_user=<user_id>')
def get_user_posts(user_id):
    return Post.user_get(user_id)

@interface.post('/posts')
def add_post():
    return Post.add()

@interface.put('/posts/<post_id>')
def update_post(post_id):
    return Post.update_post(post_id)

@interface.delete('/posts/<post_id>')
def delete_post(post_id):
    return Post.delete(post_id)