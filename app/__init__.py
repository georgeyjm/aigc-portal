from flask import Flask

from config import app_config
from app.extensions import db, cache, login_manager, jwt
from app.models import *


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(app_config['development'])
    flask_app.config.from_pyfile('secrets.py')

    # Initialize Flask extensions with app
    cache.init_app(flask_app)
    login_manager.init_app(flask_app)
    jwt.init_app(flask_app)
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.main import bp as main_bp
    from app.apis import bp as apis_bp
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(apis_bp, url_prefix='/api')

    return flask_app
