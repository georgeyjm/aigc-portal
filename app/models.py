from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    '''Model for users table.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    chats = db.relationship('Chat', back_populates='user')
    tokens = db.relationship('Token', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def authenticate(self, password):
        '''Checks if provided password matches hashed password.'''
        return check_password_hash(self.password, password)


class Token(db.Model):
    '''Model for tokens table.'''

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    platform = db.Column(db.String(64), nullable=False)
    # platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))
    token = db.Column(db.String(256), nullable=False)

    user = db.relationship('User', back_populates='tokens')

    def __repr__(self):
        return '<Token {}>'.format(self.id)


class AIGCModel(db.Model):
    '''Model for models table.'''

    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    # platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'))

    def __repr__(self):
        return '<Model {}>'.format(self.id)


class Chat(db.Model):
    '''Model for chats table.'''

    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))

    messages = db.relationship('ChatMessage', back_populates='chat')
    user = db.relationship('User', back_populates='chats')

    def __repr__(self):
        return '<Chat {}>'.format(self.id)

    def to_history(self, format='chatgpt'):
        if format == 'chatgpt':
            history = []
            for message in self.messages:
                msg = {'content': message.content}
                if message.is_user:
                    msg['role'] = 'user'
                else:
                    msg['role'] = 'assistant'
                history.append(msg)
        return history


class ChatMessage(db.Model):
    '''Model for chat messages table.'''

    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    is_user = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    chat = db.relationship('Chat', back_populates='messages')

    def __repr__(self):
        return '<ChatMessage {}>'.format(self.id)


# class Chat(db.Model):
#     '''Model for chats table.'''

#     __tablename__ = 'chats'

#     id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self):
#         return '<Chat {}>'.format(self.id)
