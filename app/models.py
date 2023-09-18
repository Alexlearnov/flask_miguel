from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class UsersView(UserMixin, db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('PostsView', backref='author', lazy='dynamic')
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(10))

    def __repr__(self):
        return f'<User {self.username} Email {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email)
class PostsView(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
    return UsersView.query.get(int(id))