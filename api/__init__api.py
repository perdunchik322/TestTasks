from flask_restful import Api
from .users_resource import UsersResource, UsersListResource

def init_api(app):
    api = Api(app)
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')