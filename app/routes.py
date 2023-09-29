from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, UserRegistrationForm, EditProfileForm, EmptyForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import UsersModel, PostsModel
from urllib.parse import urlsplit
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post: PostsModel = PostsModel(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')

        return redirect(url_for('index'))
    return render_template('index.html', title='Microblog', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user: UsersModel = UsersModel.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        flash(f'Login for user {form.username.data}, remember me {form.remember_me.data}')
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('index')
        if request.args.get('next') and urlsplit(next_page).netloc == '':
            next_page = request.args.get('next')
            if next_page == '/my_profile/':
                next_page = f"/my_profile/{user.username}"
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/log_out/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/my_profile/')
@app.route('/my_profile/<username>')
@login_required
def my_profile(username):
    user = UsersModel.query.filter_by(username=username).first_or_404()
    posts = PostsModel.query.filter_by(user_id=user.id).all()
    form = EmptyForm()
    return render_template("user_profile.html", user=user, posts=posts, title="Home", form=form,
                           )

@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)



@app.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = UsersModel(username=form.username.data,
                         email=form.email.data,
                         first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', registration=form, title='Sign Up')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('my_profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('my_profile', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('my_profile', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('my_profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/explore/')
@login_required
def explore():
    posts = PostsModel.query.order_by(PostsModel.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)