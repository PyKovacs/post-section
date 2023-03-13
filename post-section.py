from source.classes import app, db
import source.actions
import os


def main():
    #Initialize DB
    if not os.path.exists('./data/data.db'):
        os.mkdir("./data")
        db.create_all()

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


if __name__ == 'post-section':
    main()


'''
TO IMPROVE: 
- DB INIT ON START
- SWAGGER DOCU
- CODE STRUCTURE REVIEW
    - wrap app to class
- FRONTEND HTML,CSS
- PACKAGING
- README
'''