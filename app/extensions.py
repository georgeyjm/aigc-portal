from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache


db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
