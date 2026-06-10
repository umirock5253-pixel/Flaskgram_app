from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

follows = db.Table('follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.String(300), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    liked_posts = db.relationship('Post', secondary=likes, backref='liked_by', lazy=True)
    following = db.relationship('User', secondary=follows,
                                primaryjoin=(follows.c.follower_id == id),
                                secondaryjoin=(follows.c.followed_id == id),
                                backref='followers', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio
        }

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date_posted': str(self.date_posted),
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Post {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))