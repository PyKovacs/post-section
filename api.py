from flask import Blueprint

from source.model import Post

api_interface = Blueprint(__name__, 'api_interface')
post_model = Post()

@api_interface.get('/posts/<post_id>')
def get_post(post_id):
    '''Get post based on post id.'''
    return Post.get(post_id)

@api_interface.get('/posts/from_user=<user_id>')
def get_user_posts(user_id):
    '''Get posts based on user id.'''
    return Post.user_get(user_id)

@api_interface.post('/posts')
def add_post():
    '''Add post.'''
    return Post.add()

@api_interface.put('/posts/<post_id>')
def update_post(post_id):
    '''Update post.'''
    return Post.update(post_id)

@api_interface.delete('/posts/<post_id>')
def delete_post(post_id):
    '''Delete post.'''
    return Post.delete(post_id)