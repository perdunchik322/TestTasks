from flask import jsonify, make_response, render_template
from data import db_session
from flask import jsonify
from .blueprint import api_blueprint
from data.jobs import Jobs
from flask import request
from datetime import datetime

@api_blueprint.route('/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify({'jobs': [job.to_dict() for job in jobs]})

@api_blueprint.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({'job': job.to_dict()})

from datetime import datetime

@api_blueprint.route('/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    
    db_sess = db_session.create_session()
    
    start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d')
    
    jobs = Jobs(
        team_leader_id=request.json['team_leader_id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=start_date,
        end_date=end_date,
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})