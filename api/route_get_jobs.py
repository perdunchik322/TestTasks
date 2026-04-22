from flask import jsonify, render_template
from data import db_session
from flask import jsonify
from .blueprint import jobs_blueprint
from data.jobs import Jobs

@jobs_blueprint.route('/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({'jobs': [job.to_dict() for job in jobs]})