from functools import wraps
from app import app
from flask import jsonify,request,session
from app.md.models import User
import jwt

from app.md.models import User
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
       
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # btoken = blacklist.query.filter_by(token=token).first()
        # if btoken:
        #     return jsonify({'Message':'Token has been blacklisted,please login again'}),401
        # if not token:
        #     return jsonify({'message' : 'Token is missing!'})

        
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"],options=None)
                
            if current_user.id != session["user_id"]:
                return jsonify({'message' : 'Token is invalid!'})
        except:
            return jsonify({'message' : 'Token is invalid!'})

        return f(current_user)

    return decorated