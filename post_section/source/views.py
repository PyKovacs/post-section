from flask import Response

from post_section import app
from post_section.source.model import Post

post_model = Post()


@app.get('/posts/<post_id>')
def get_post(post_id) -> tuple[dict[str, int | str], int]:
    """Get post based on post id."""
    return Post.get(post_id)


@app.get('/posts/from_user=<user_id>')
def get_user_posts(user_id) -> tuple[(Response | dict[str, int | str]), int]:
    """Get posts based on user id."""
    return Post.user_get(user_id)


@app.post('/posts')
def add_post() -> tuple[dict[str, int | str], int]:
    """Add post."""
    return Post.add()


@app.put('/posts/<post_id>')
def update_post(post_id) -> tuple[dict[str, dict[str, int | str]], int]:
    """Update post."""
    return Post.update(post_id)


@app.delete('/posts/<post_id>')
def delete_post(post_id) -> tuple[dict[str, str], int]:
    """Delete post."""
    return Post.delete(post_id)
