from flask import jsonify, request
from source.classes import Post, ExAPI, db


def get_post(post_id):
    '''
    Performs GET request with post ID as parameter.
    Example url: http://127.0.0.1:5000/posts/104

    If post not found, search for post on external API.
    '''
    try:
        post = Post.query.get(post_id)
        return post.show()
    except AttributeError:
        posts_ext_api = ExAPI('posts/')
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


def get_user_posts(user_id):
    '''
    Performs GET request with user ID as parameter.
    Example url: http://127.0.0.1:5000/posts/from_user=9
    '''
    result = Post.query.filter(Post.userId == user_id)
    post_ids = result.all()
    posts = []
    for post_id in post_ids:
        post = Post.query.get(str(post_id))
        posts.append(post.show())
    if not posts:
        return {'msg': 'No posts from user {}'.format(user_id)}, 404
    return jsonify(posts)


def add_post():
    '''
    Performs POST request. Request must contain data.
    Example url: http://127.0.0.1:5000/posts

    User ID is validated against external API.
    '''
    check = Post.input_validation(request)
    if check[1] != 0:
        return check
    req = check[0]

    # user validation on external API
    users_ext_api = ExAPI('users/')
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


def update_post(post_id):
    '''
    Performs PUT request with post ID as parameter.
    Request must contain data.
    Example url: http://127.0.0.1:5000/posts/104
    '''

    # find post
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404

    # data validation
    check = Post.input_validation(request, 'update_post')
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


def delete_post(post_id):
    '''
    Performs DELETE request with post ID as parameter.
    Example url: http://127.0.0.1:5000/posts/104
    '''
    post = Post.query.get(post_id)
    if post is None:
        return {'msg': 'Post ID {} not found.'.format(post_id)}, 404
    db.session.delete(post)
    db.session.commit()
    return {'msg': 'Post with ID {} deleted.'.format(post_id)}, 200
