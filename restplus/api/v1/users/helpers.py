from flask_restplus import Resource

from restplus.models import UpdateError, Post, User
from ..helpers import validate, get_namespace, json_checker, safe_post_output


def extract_post_data(resource: Resource, method: str):
    api = resource.api
    namespace = get_namespace(api, resource)
    json_checker(api, namespace)

    payload = api.payload
    title = payload.get('title')
    body = payload.get('body')

    if method == 'post':
        validate('title', title, namespace)
        validate('body', body, namespace)
    elif method == 'patch':
        if title:
            validate('title', title, namespace)
        if body:
            validate('body', body, namespace)

        if not body and not title:
            namespace.abort(400)

    return title, body


def generate_post_output(resource: Resource, post: Post, method: str):
    output_dict = dict(post=safe_post_output(resource, post))

    if resource.endpoint == 'users_single_user_all_posts':
        if method == 'post':
            output_dict['message'] = 'post created successfully'
    elif resource.endpoint == 'users_single_user_single_post':
        if method == 'patch':
            output_dict['message'] = 'post modified successfully'

    return output_dict


def patch_post(resource, item_pair: tuple, user: User, post: Post):
    api = resource.api
    namespace = get_namespace(api, resource)
    name, item = item_pair
    try:
        modified_post = user.update_post(name, item, post)
        return modified_post
    except UpdateError as e:
        error = e.args[0]
        namespace.abort(400, error)
