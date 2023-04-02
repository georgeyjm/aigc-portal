from flask import Response, request, send_from_directory, render_template, jsonify, redirect, url_for, make_response, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_
import jwt

from app.main import bp
from app.extensions import db
from app.models import User
# from app.aigc import *
from app.utils import browser_cache, return_error_html


@bp.route('/')
@browser_cache(3600)
@return_error_html
def index_page():
    return render_template('index.html')


@bp.route('/chat')
@return_error_html
def chat_page():
    return render_template('chat.html')


@bp.route('/login', methods=['GET', 'POST'])
@return_error_html
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('search_page'))
        else:
            return render_template('login.html')
        
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_obj = User.query.filter_by(username=username).first()
        if user_obj.authenticate(password):
            access_token = create_access_token(identity=user_obj.id)
            return jsonify({'token': access_token})


@bp.route('/register', methods=['GET', 'POST'])
@return_error_html
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('search_page'))
        else:
            return render_template('login.html')
        
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # TODO: Check for duplicate username
        user_obj = User(username=username, password=generate_password_hash(password))
        db.session.add(user_obj)
        db.session.commit()
        return jsonify({'code': 0, 'data': {'user_id': user_obj.id}})


@bp.route('/logout')
@return_error_html
def logout_page():
    logout_user()
    return redirect(url_for('search_page'))
