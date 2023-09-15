from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, UserRegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import UsersView
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Microblog')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user: UsersView = UsersView.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        flash(f'Login for user {form.username.data}, remember me {form.remember_me.data}')
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('index')
        if next_page and urlsplit(next_page).netloc == '':
            next_page = request.args.get('next')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/log_out/')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/my_profile/')
@login_required
def my_profile():
    return render_template("user_profile.html", title="Home")


@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = UsersView(username=form.username.data,
                         email=form.email.data,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', registration=form)