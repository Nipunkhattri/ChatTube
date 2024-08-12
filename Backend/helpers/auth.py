from flask import g, request
from functools import wraps
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt,
    create_access_token, create_refresh_token
)
from responses import BaseResponse
from logger import logger
from helpers.error_codes import error_codes
from models import User
from database import db

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # verify the JWT token
            verify_jwt_in_request()
            claims = get_jwt()
        except Exception as e:
            logger.debug(e)
            return BaseResponse.unauthorized(1005,error_codes[1005])

        user = User.query.filter(
            User.id == claims.get("sub")
        ).first()

        if not user:
            return BaseResponse.forbidden(1006,error_codes[1006])

        # set the user in the global context
        g.user = user
        return f(*args, **kwargs)

    return decorated
