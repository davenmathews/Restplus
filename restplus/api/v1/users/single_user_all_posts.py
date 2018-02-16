from flask import url_for
from flask_login import current_user, login_required
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from restplus.api.v1.users.helpers import extract_post_data, generate_post_output
from restplus.models import users_list, posts_list

users_ns = Namespace('users')
post_model = users_ns.model('post_model', {
    'title': fields.String(title='The title of your post', required=True,
                           example='My Post Title'),
    'body': fields.String(title='The body of your post', required=True,
                          example='Something interesting for people to read.')
})


class SingleUserAllPosts(Resource):

    def get(self, user_id):
        pass

    @users_ns.expect(post_model)
    @login_required
    def post(self, user_id):
        for a_user in users_list:
            if a_user.id == user_id:
                break
        else:
            users_ns.abort(400, 'user not found')

        if current_user.id != user_id:
            users_ns.abort(401)

        title, body = extract_post_data(self)
        for a_post in posts_list:
            if a_post.title == title and a_post.body == body:
                users_ns.abort(400, 'post already exists')

        post = current_user.create_post(title, body)
        output = generate_post_output(self, post, 'post')
        response = self.api.make_response(output, 201)
        response.headers['location'] = url_for(self.api.endpoint('users_single_user_single_post'),
                                               user_id=post.user_id, post_id=post.id)
        return response

    def delete(self, user_id):
        pass
