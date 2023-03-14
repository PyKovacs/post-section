from flask import Blueprint, Response

from source.model import Post

api_interface = Blueprint('api_interface', __name__)
post_model = Post()

@api_interface.get('/posts/<post_id>')
def get_post(post_id) -> tuple[dict[str, (int|str)], int]:
    '''Get post based on post id.'''
    return Post.get(post_id)

@api_interface.get('/posts/from_user=<user_id>')
def get_user_posts(user_id) -> tuple[(Response | dict[str, (int|str)]), int]:
    '''Get posts based on user id.'''
    return Post.user_get(user_id)

@api_interface.post('/posts')
def add_post() -> tuple[dict[str, (int|str)], int]:
    '''Add post.'''
    return Post.add()

@api_interface.put('/posts/<post_id>')
def update_post(post_id) -> tuple[dict[str, dict[str, (int|str)]], int]:
    '''Update post.'''
    return Post.update(post_id)

@api_interface.delete('/posts/<post_id>')
def delete_post(post_id) -> tuple[dict[str, str], int]:
    '''Delete post.'''
    return Post.delete(post_id)