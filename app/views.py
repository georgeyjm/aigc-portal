import sys
from functools import wraps

from flask import Response, request, send_from_directory, render_template, jsonify, redirect, url_for, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from app import app, db, login_manager
from app.models import *
from sqlalchemy import and_, or_



#################### Misc ####################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_redirect():
    return redirect('/login?url=' + request.path)


def return_error_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, __, exc_tb = sys.exc_info()
            return jsonify({'code': -1, 'error': '{}: {}'.format(e.__class__.__name__, e), 'line': exc_tb.tb_lineno})
    return wrapper


def return_error_html(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, __, exc_tb = sys.exc_info()
            return render_template('error.html', error_msg='({}) {}: {}'.format(exc_tb.tb_lineno, e.__class__.__name__, e))
    return wrapper


def browser_cache(seconds):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            if not isinstance(resp, Response):
                resp = make_response(resp)
            # Not setting 'Expires' because everyone is already using HTTP/1.1 now
            resp.headers['Cache-Control'] = 'public, max-age={}'.format(seconds)
            return resp
        return wrapper
    return outer_wrapper


#################### Web Pages ####################


@app.route('/')
@browser_cache(3600)
@return_error_html
def search_page():
    return render_template('search.html')


@app.route('/login')
@return_error_html
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('search_page'))
    else:
        return render_template('login.html')


@app.route('/logout')
@return_error_html
def logout_page():
    logout_user()
    return redirect(url_for('search_page'))
