from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
jwt = JWTManager()
