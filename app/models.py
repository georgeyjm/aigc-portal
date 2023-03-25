from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app import db, login_manager


class Rating(db.Model):
    '''Model for ratings table.'''

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('ratings.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    ups = db.Column(db.Integer, nullable=False, default=0)
    downs = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Rating {}>'.format(self.id)
