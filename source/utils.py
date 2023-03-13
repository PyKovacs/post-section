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
