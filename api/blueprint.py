import flask

jobs_blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='../templates',
    static_folder='../static',
    url_prefix='/api'
)
