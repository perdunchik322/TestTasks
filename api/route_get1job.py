from flask import jsonify, render_template
from data import db_session
from flask import jsonify
from .blueprint import jobs_blueprint
from data.jobs import Jobs

@jobs_blueprint.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({'job': job.to_dict()})