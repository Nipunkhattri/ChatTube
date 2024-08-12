from flask import Blueprint
from flask_restx import Api
from config import Config
from views.auth import auth_api
from views.llm import llm_api

blueprint = Blueprint("api", "flask backend")
api = Api(blueprint, title='Apis', version='1.0', docs=Config.DEBUG)

api.add_namespace(auth_api)
api.add_namespace(llm_api)