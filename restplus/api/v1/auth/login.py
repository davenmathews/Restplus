from flask_login import login_user, LoginManager, current_user
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from restplus.api.v1.auth.helpers import extract_auth_data, generate_auth_output
from restplus.models import users_list

auth_ns = Namespace('auth')

login_manager = LoginManager()

user_login_model = auth_ns.model('user_login', {
    'email': fields.String(title='Your email address', required=True,
                           example='myemail@company.com'),
    'password': fields.String(title='Your email address', required=True,
                              example='password.Pa55word')
})


@login_manager.user_loader
def load_user(user_id):
    for a_user in users_list:
        # In the session, user_id is stored as a unicode character
        # The chr() converts the int id of the user found to unicode for comparing equality
        if chr(a_user.id) == user_id:
            return a_user


class Login(Resource):
    @auth_ns.expect(user_login_model)
    @auth_ns.response(200, 'user logged in successfully')
    @auth_ns.response(415, 'request data not in json format')
    @auth_ns.response(401, 'invalid password')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User Login

        Makes use of Flask-Login

        Use the correct user information to login. Guidelines as stipulated in the register route should be followed

        Note: Only one user can be logged in per client

        """
        try:
            return {'message': current_user.email + ' is currently logged in'}, 400
        except AttributeError:
            pass

        email, password = extract_auth_data(self)
        for a_user in users_list:
            if email == a_user.email:
                if a_user.authenticate(password):
                    login_user(a_user)
                    output = generate_auth_output(self, a_user)
                    response = self.api.make_response(output, 200)
                    return response
                else:
                    auth_ns.abort(401, 'invalid password')
            else:
                continue
        else:
            auth_ns.abort(400, 'user not found!')
