from pydantic import field_validator , BaseModel , EmailStr

class UserRegistrationData(BaseModel):

    email:EmailStr
    password:str
    
class UserLoginData(BaseModel):

    email:EmailStr
    password:str
