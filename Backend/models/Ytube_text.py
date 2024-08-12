from database import db,ma
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON 

class Ytube_text(db.Model):
    __tablename__ = 'Ytube_text'

    id = db.Column(db.String,primary_key=True)
    extracted_text = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    chat_history = db.Column(JSON, nullable=True)
    in_process = db.Column(db.Boolean,nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

class Ytube_text_Schema(ma.Schema):
    class Meta:
        fields = ('id','extracted_text')
        model = Ytube_text