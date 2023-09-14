from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import UsersView


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Microblog')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user: UsersView = UsersView.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        flash(f'Login for user {form.username.data}, remember me {form.remember_me.data}')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/log_out/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/my_profile/')
def my_profile():
    return render_template("user_profile.html", title="Home")
