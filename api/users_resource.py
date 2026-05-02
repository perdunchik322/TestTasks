from flask import jsonify, make_response, render_template
from data import db_session
from data.jobs import Jobs
from flask import request
from datetime import datetime
from flask_restful import reqparse, abort, Resource
from data.user import User
from . import api_parser

def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message="User not found")
    session.close()

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        result = [user.to_dict() for user in users]
        session.close()
        return jsonify({'users': result})

    def post(self):
        args = api_parser.parser.parse_args()
        session = db_session.create_session()
        user = User(name=args['name'], 
                    surname=args['surname'],
                    age=args['age'],
                    position=args['position'],
                    speciality=args['speciality'],
                    address=args['address'],
                    email=args['email'],
                    modified_date=args['modified_date'])
        session.add(user)
        session.commit()
        session.close()

        return jsonify({'success': 'OK'})

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        result = user.to_dict()
        session.close()
        return jsonify({'user': result})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})