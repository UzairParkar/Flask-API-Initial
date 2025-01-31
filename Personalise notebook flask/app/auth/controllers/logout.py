from flask_restful import Resource
from flask_jwt_extended import get_jwt
from flask import jsonify, request
# from app.auth.decorators import blacklist
from app import db
# from app.md.models import blacklist
# from app.md.serde import blacklistSchema
import jwt
from flask import session
from app import app

# class LogOutView(Resource):
#     def post(self):
#         token = request.headers.get('x-access-token')
#         if not token:
#             return jsonify({'Message':'Token is missing'}),400
#         # decoded_token =jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
#         existing_token = blacklist.query.filter_by(token = token).first()

#         if existing_token:
#             return jsonify({'Message':'Token already Blacklisted'}) 
#         btoken = blacklist(token = token)
#         db.session.add(btoken)
#         blacklistSchema().dump(btoken)
#         return jsonify({'Message':'Logged Out Sucessfully'}),200

'''Was trying to work with Blacklist'''

class LogOutView(Resource):
    def post(self):
        session.pop('user_id',None)
        return jsonify({'Message':'Logged Out Sucesfully'})
        

    

        

