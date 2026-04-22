from flask import render_template
from data import db_session
from .blueprint import jobs_blueprint
from data.jobs import Jobs