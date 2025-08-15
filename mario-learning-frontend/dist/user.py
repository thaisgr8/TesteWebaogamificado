from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ldap_username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatar.id'), nullable=True)
    score = db.Column(db.Integer, default=0)
    progress = db.Column(db.Float, default=0.0)  # Progresso em porcentagem
    time_spent = db.Column(db.Integer, default=0)  # Tempo em segundos
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    avatar = db.relationship('Avatar', backref='users')
    user_progress = db.relationship('UserProgress', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.ldap_username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ldap_username': self.ldap_username,
            'email': self.email,
            'avatar_id': self.avatar_id,
            'score': self.score,
            'progress': self.progress,
            'time_spent': self.time_spent,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Avatar {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url
        }

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    order = db.Column(db.Integer, nullable=False)

    # Relacionamentos
    modules = db.relationship('Module', backref='world', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<World {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'order': self.order
        }

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)

    # Relacionamentos
    activities = db.relationship('Activity', backref='module', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Module {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'world_id': self.world_id,
            'title': self.title,
            'content': self.content,
            'order': self.order
        }

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    incorrect_answer = db.Column(db.Text, nullable=False)
    score_value = db.Column(db.Integer, default=10)

    def __repr__(self):
        return f'<Activity {self.question[:50]}...>'

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'question': self.question,
            'correct_answer': self.correct_answer,
            'incorrect_answer': self.incorrect_answer,
            'score_value': self.score_value
        }

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)

    # Relacionamentos
    module = db.relationship('Module', backref='user_progress')

    def __repr__(self):
        return f'<UserProgress User:{self.user_id} Module:{self.module_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'completed': self.completed,
            'score': self.score,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

