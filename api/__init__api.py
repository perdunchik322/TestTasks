from flask_restful import Api

from .jobs_resource import JobsResource, JobsListResource
from .users_resource import UsersResource, UsersListResource

def init_api(app):
    api = Api(app)
    api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(JobsListResource, '/api/v2/jobs')
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')