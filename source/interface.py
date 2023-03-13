from typing import Protocol

'''
Plan is to isolate control plane here, then use this interface classes in views.
'''


class InterfaceController(Protocol):
    '''
    Handles the requests and trigger corresponding actions.
    '''

    def get_post(post_id):
        '''
        Performs GET request with post ID as parameter.
        Example url: http://127.0.0.1:5000/posts/104

        If post not found, search for post on external API.
        '''
        raise NotImplementedError

    def get_user_posts(user_id):
        '''
        Performs GET request with user ID as parameter.
        Example url: http://127.0.0.1:5000/posts/from_user=9
        '''
        raise NotImplementedError


    def add_post():
        '''
        Performs POST request. Request must contain data.
        Example url: http://127.0.0.1:5000/posts

        User ID is validated against external API.
        '''
        raise NotImplementedError


    def update_post(post_id):
        '''
        Performs PUT request with post ID as parameter.
        Request must contain data.
        Example url: http://127.0.0.1:5000/posts/104
        '''
        raise NotImplementedError

    def delete_post(post_id):
        '''
        Performs DELETE request with post ID as parameter.
        Example url: http://127.0.0.1:5000/posts/104
        '''
        raise NotImplementedError
    
