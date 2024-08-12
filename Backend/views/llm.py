from flask_restx import Namespace,Resource
from helpers.error_codes import error_codes
from helpers.auth import login_required
from responses import BaseResponse
from database import db
from flask import request,g
import random
import string
from config import Config
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from celery_tasks.collections.tasks import extract_text_and_create_embeddings
from models.Ytube_text import Ytube_text
from helpers.Query_Data import GetQueryResponse
from models.Ytube_text import Ytube_text_Schema

llm_api = Namespace('llm',description='Creating embedding and saving in chroma db')

def generate_random_string_id(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# celery task which will extract text and create embeddings
@llm_api.route('/extract_text')
class ExtractText_Embeddings(Resource):
    @login_required
    def post(self):
        """
            celery task which will extract text and create embeddings
        """
        data = request.get_json()
        
        random_string_id = generate_random_string_id(5)  # Generate a random string of length 5
        user_id = g.user.id

        # create data in db using random string id
        new_video = Ytube_text(
            id = random_string_id,
            extracted_text = '',
            user_id = user_id,
            in_process = True
        )
        db.session.add(new_video)

        db.session.commit()

        Youtube_link = data['Youtube_link']
    
        extract_text_and_create_embeddings.delay(random_string_id,user_id,Youtube_link)

        return BaseResponse.success({
            "id":random_string_id
        })

# check that celery task is finished or not? 
@llm_api.route('/<string:id>')
class check_text_extracted(Resource):
    @login_required
    def get(self,id):
        """
        check that celery task is finished or not? 
        """
        data = Ytube_text.query.filter_by(id=id).first()

        if data is None:
            return BaseResponse.bad_request(1003,error_codes[1003])

        if data.in_process == False:
            return BaseResponse.success({
                'message':'Extracted Successfully'
            })
        else :
            return BaseResponse.bad_request(1004,error_codes[1004])

@llm_api.route('/getHistory/<string:id>')
class check_text_extracted(Resource):
    @login_required
    def get(self,id):
        """
        check that celery task is finished or not? 
        """
        data = Ytube_text.query.filter_by(id=id).first()
        
        chat_history = data.chat_history

        return BaseResponse.success({
            "chathistory":chat_history
        })
# get all ids for that user

@llm_api.route('/GetallIds')
class GetAllIds(Resource):
    @login_required
    def get(self):

        data = Ytube_text.query.all()
        Ids = Ytube_text_Schema(many=True).dump(data)
        return Ids

# take query and id and return the result
@llm_api.route('/query')
class QueryText(Resource):
    @login_required
    def post(self):
        """
        take query and id and return the result
        """
        data = request.get_json()
        id = data['id']
        query=data['query']
        print(id)
        data = Ytube_text.query.filter_by(id=id).first()
        print(data)
        response_text,chat_history = GetQueryResponse(id=id, customer_query=query)

        data.chat_history = chat_history

        db.session.commit()

        return BaseResponse.success({
            "response":response_text,
            "chathistory":chat_history
        })