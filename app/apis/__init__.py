from flask import Blueprint

bp = Blueprint('apis', __name__)

from app.apis import views
