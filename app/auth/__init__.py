from flask import Blueprint

auth = Blueprint("user", __name__)


from . import views, controllers
