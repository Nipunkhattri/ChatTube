from typing import Any, Optional
from flask import jsonify

class BaseResponse:
    """
    Base response model for all API responses
    """
    status_code: Optional[int]
    message: Optional[str]
    error: Optional[str]
    data: Optional[Any]

    @classmethod
    def success(cls, data: Any, message: str = "Success", status_code: int = 200):
        response = jsonify({
            "message": message,
            "data": data
        })
        response.status_code = status_code
        return response

    @classmethod
    def created(cls, message: str = "Created", status_code: int = 201):
        response = jsonify({
            "message": message
        })
        response.status_code = status_code
        return response

    @classmethod
    def internal_server_error(cls, error_code: int, error: str = "Internal Server Error", details: dict = None, status_code: int = 500):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @classmethod
    def bad_request(cls, error_code: int, error: str = "Bad Request", details: dict = None, status_code: int = 400):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @classmethod
    def unauthorized(cls, error_code: int, error: str = "Unauthorized", details: dict = None, status_code: int = 401):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @classmethod
    def forbidden(cls, error_code: int, error: str = "Forbidden", details: dict = None, status_code: int = 403):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @classmethod
    def not_found(cls, error_code: int, error: str = "Not Found", details: dict = None, status_code: int = 404):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @classmethod
    def unprocessable_entity(cls, error_code: int, error: str = "Unprocessable Entity", details: dict = None, status_code: int = 422):
        response = jsonify(BaseResponse.generate_error_json_response(
            error_code, error, details))
        response.status_code = status_code
        return response

    @staticmethod
    def generate_error_json_response(error_code: int, error: str, details: dict = None):
        json_response = {
            "error": error,
            "error_code": error_code
        }
        if details:
            json_response.update({"details": details})
        return json_response