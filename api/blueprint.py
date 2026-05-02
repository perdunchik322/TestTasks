import flask

api_blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='../templates',
    static_folder='../static',
    url_prefix='/api'
)
