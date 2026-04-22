from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, current_user
from data.user import User
from data.jobs import Jobs
from data import db_session
import flask
from flask_login import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdsafsd'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

@app.route('/')
@login_required
def main():
    session = db_session.create_session()
    logs = session.query(Jobs).all()
    return render_template('table.html', logs=logs)

class AuthForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')

    login = SubmitField('Войти')
    register = SubmitField('Зарегистрироваться')

class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    
    submit = SubmitField('Сохранить')

class AddJobForm(FlaskForm):
    job = StringField('Задача', validators=[DataRequired()])
    work_size = IntegerField("Объём работы", validators=[DataRequired()])
    collaborators = StringField("Сотрудники", validators=[DataRequired()])
    start_date = DateTimeField("Дата начала", validators=[DataRequired()])
    end_date = DateTimeField("Дата дедлайна", validators=[DataRequired()])
    is_finished = BooleanField("Закончена ли")
    submit = SubmitField("Сохранить")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthForm()
    message = ""

    db_sess = db_session.create_session()
    if form.is_submitted():
        print("ОШИБКИ ФОРМЫ:", form.errors)
    if form.validate_on_submit():

        if form.login.data:
            user = db_sess.query(User).filter(
                User.email == form.email.data
            ).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect('/')

            message = "Неверный логин или пароль"

        elif form.register.data:

            if db_sess.query(User).filter(User.email == form.email.data).first():
                message = "Пользователь уже существует"
            else:
                user = User(email=form.email.data)
                user.set_password(form.password.data)

                db_sess.add(user)
                db_sess.commit()

                login_user(user) 
                return redirect('/')

    return render_template('login.html', form=form, message=message)

@app.route('/add_job', methods=["GET", 'POST'])
def add_job():
    form = AddJobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        job = Jobs(
            team_leader_id=current_user.id,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()

        return redirect("/jobs")

    return render_template("add_job.html", form=form)
@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.get(Jobs, job_id)

    if not job:
        return "Задача не найдена"
    
    if job.team_leader_id != current_user.id or current_user.id != 1:
        return "У вас нет прав для редактирования этой задачи", 403

    form = AddJobForm(obj=job)

    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data

        db_sess.commit()
        return redirect("/jobs")

    return render_template("edit_job.html", form=form, job_id=job_id)

@app.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    form = RegisterForm(obj=current_user)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.get(User, current_user.id)

        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            db_sess.commit()

            return redirect('/')

    return render_template('complete_profile.html', form=form)

@app.route('/jobs')
@login_required
def jobs():
    db_sess = db_session.create_session()
    jobs_for_user = db_sess.query(Jobs).filter(
        Jobs.team_leader_id == current_user.id
    ).all()

    return render_template("jobs.html", jobs_for_user=jobs_for_user)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(host='127.0.0.1', port=8080, debug=True)