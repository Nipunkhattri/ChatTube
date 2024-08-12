from flask_restx import Namespace,Resource
from helpers.error_codes import error_codes
from responses import BaseResponse
from database import db
from flask import request,g
from request_parsers.user import UserRegistrationData,UserLoginData
from config import Config
from flask_jwt_extended import (
    create_access_token, create_refresh_token
)
from query.auth_query import AuthQuery

auth_api = Namespace('auth',description='User related operations')

# Register the User
@auth_api.route('/register')
class Register(Resource):
    def post(self):
        """
        endpoint to register a new user
        """
        data = request.get_json()

        try:
            user = UserRegistrationData(**data)
        except Exception as e:
            return BaseResponse.bad_request(1011, str(e))

        user_exist = None

        user_exist = AuthQuery.get_user_by_email(db,email=data['email'])

        if user_exist:
            return BaseResponse.bad_request(1001,error_codes[1001])
        
        # Adding New User
        new_user = AuthQuery.add_user_to_database(db,password=user.password,email=data['email'])
        db.session.commit()

        access_token = create_access_token(
            identity=new_user.id, fresh=True, expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES)

        return BaseResponse.success({
            "access_token": access_token,
        }, message="User created successfully")

# Login the User
@auth_api.route('/login')
class Login(Resource):
    def post(self):
        """
        Endpoint to login user
        """
        data = request.get_json()

        try:
            user = UserLoginData(**data)
        except Exception as e:
            return BaseResponse.bad_request(1011,str(e))
        
        user_exist = None

        # check user exist
        user_exist = AuthQuery.get_user_by_email(db,email=data['email'])

        if user_exist is None:
            return BaseResponse.bad_request(1002, error_codes[1002])
        
        access_token = create_access_token(
            identity=user_exist.id, fresh=True, expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES)
        refresh_token = create_refresh_token(
            identity=user_exist.id, expires_delta=Config.JWT_REFRESH_TOKEN_EXPIRES)

        return BaseResponse.success({
            "access_token": access_token,
            "refresh_token": refresh_token
        }, message="User logged in successfully")