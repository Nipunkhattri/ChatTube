from database import db
from models import User

class AuthQuery:
    
    @staticmethod
    def get_user_by_email(db,email):
        user_exists = User.query.filter_by(email=email).first()
        return user_exists
    
    @staticmethod
    def add_user_to_database(db,password,email):
        new_user = User(
            password = password,
            email = email
        )
        db.session.add(new_user)
        return new_user