from flask import jsonify, request
from utils import Post, ExAPI, app, db, input_validation


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
