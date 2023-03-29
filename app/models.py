from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    '''Model for users table.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def authenticate(self, password):
        '''Checks if provided password matches hashed password.'''
        return check_password_hash(self.password, password)


class Tokens(db.Model):
    '''Model for tokens table.'''

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    platform = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<Token {}>'.format(self.name)


class Chat(db.Model):
    '''Model for chats table.'''

    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Chat {}>'.format(self.id)


class ChatMessage(db.Model):
    '''Model for chat messages table.'''

    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<ChatMessage {}>'.format(self.id)


# class Chat(db.Model):
#     '''Model for chats table.'''

#     __tablename__ = 'chats'

#     id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self):
#         return '<Chat {}>'.format(self.id)
