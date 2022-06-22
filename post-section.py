from source.classes import app
import source.actions

@app.get('/posts/<post_id>')
def get_post(post_id):
    return source.actions.get_post(post_id)


@app.get('/posts/from_user=<user_id>')
def get_user_posts(user_id):
    return source.actions.get_user_posts(user_id)


@app.post('/posts')
def add_post():
    return source.actions.add_post()


@app.put('/posts/<post_id>')
def update_post(post_id):
    return source.actions.update_post(post_id)


@app.delete('/posts/<post_id>')
def delete_post(post_id):
    return source.actions.delete_post(post_id)
