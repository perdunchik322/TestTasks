from flask import jsonify, make_response, render_template
from data import db_session
from data.jobs import Jobs
from flask import request
from datetime import datetime
from flask_restful import reqparse, abort, Resource
from data.user import User
from . import api_parser

def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        abort(404, message="Job not found")
    session.close()

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        result = []
        for job in jobs:
            j = job.to_dict()
            # format datetimes as YYYY-MM-DD if present
            if isinstance(j.get('start_date'), str):
                # already serialized
                pass
            else:
                if job.start_date:
                    j['start_date'] = job.start_date.strftime('%Y-%m-%d')
                else:
                    j['start_date'] = None
                if job.end_date:
                    j['end_date'] = job.end_date.strftime('%Y-%m-%d')
                else:
                    j['end_date'] = None

            # include team_leader_id explicitly
            j['team_leader_id'] = job.team_leader_id
            result.append(j)
        session.close()
        return jsonify({'jobs': result})

    def post(self):
        args = api_parser.parser.parse_args()

        required = ['team_leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']
        if not all(args.get(k) is not None for k in required):
            abort(400, message="Bad request")

        session = db_session.create_session()

        # validate team_leader_id
        try:
            team_leader_id = int(args['team_leader_id'])
        except Exception:
            session.close()
            abort(400, message="Bad team_leader_id")

        if team_leader_id <= 0 or not session.get(User, team_leader_id):
            session.close()
            abort(400, message="Bad team_leader_id")

        # validate work_size
        try:
            work_size = int(args['work_size'])
        except Exception:
            session.close()
            abort(400, message="Bad work_size")

        # parse dates
        try:
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d')
        except Exception:
            session.close()
            abort(400, message="Bad date format, expected YYYY-MM-DD")

        # parse is_finished to boolean
        is_finished = args['is_finished']
        if isinstance(is_finished, str):
            is_finished = is_finished.lower() in ('true', '1', 'yes')

        job = Jobs(team_leader_id=team_leader_id,
                   job=args['job'],
                   work_size=work_size,
                   collaborators=args['collaborators'],
                   start_date=start_date,
                   end_date=end_date,
                   is_finished=is_finished)
        session.add(job)
        session.commit()
        session.close()

        return jsonify({'success': 'OK'})

class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        result = job.to_dict()
        if job.start_date:
            result['start_date'] = job.start_date.strftime('%Y-%m-%d')
        else:
            result['start_date'] = None
        if job.end_date:
            result['end_date'] = job.end_date.strftime('%Y-%m-%d')
        else:
            result['end_date'] = None
        result['team_leader_id'] = job.team_leader_id
        session.close()
        return jsonify({'job': result})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})