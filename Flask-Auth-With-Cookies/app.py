from flask import Flask, request,jsonify,abort, session, make_response
from datetime import datetime, timedelta, timezone 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/jwtc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    __tablename__ = "User"
    _table_args__ = (
        db.CheckConstraint(
            "length(name) >= 3 AND length(name) <=64",name = "user_name_check"
        ),
        db.CheckConstraint(
            "length(name) >=3 AND length(username) <= 32",
            name = "user_username_check"
            ),

        db.CheckConstraint(
            "length(email) >= AND length(email) <= 64",name = "user_email_check"
        ),
        db.UniqueConstraint('email')

        )

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    email = db.Column(db.String(150),unique = True)
    _password = db.Column(db.String(5550))


    @property
    def password(self):
        raise AttributeError("cannot read password")
    
    @password.setter
    def password(self,password):
        self._password = generate_password_hash(password)
        

    def verify_password(self,password):
        return check_password_hash(self._password,password)

class Userschema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    username = fields.Str()
    email = fields.Str()


def token_req(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = None
        token = request.cookies.get('currentUser')
        if not token:
            return jsonify({'Message':'Cannot Find the Token'})
        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = Users.query.filter_by(id=data['user_id']).first()
            if current_user.id != session['user_id']:
                return jsonify({'Message':'Token is Invalid'})
        except:
            return jsonify({'Message':'Token is Invalid'})
        

        return func(current_user)
    return decorated

@app.route('/login',methods=['POST'])
def login():
    credentials = request.get_json()
    user = Users.query.filter_by(username= credentials['username']).first()
    session['user_id'] = user.id
    if not user:
        abort(401)
    
    if not user.verify_password(credentials['password']):
        abort(401)

    token = jwt.encode({'user_id':user.id,'exp':datetime.utcnow() + timedelta(minutes=10)},app.config['SECRET_KEY'],algorithm="HS256")
    response = make_response(token)
    response.set_cookie(
        'currentUser',token,secure=app.config.get("SECURE_COOKIE")
    )
    return response

@app.route('/signup',methods = ['POST'])
def signup():
    data = request.get_json()
    existing_username = Users.query.filter_by(username=data['username']).count()
    existing_email = Users.query.filter_by(email = data['email']).count()

    if existing_username:
        raise({"username":"Username is already in use"})

    if existing_email:
        raise({'email':'Email is already in use'})

    if len(data['name']) < 2:
        raise({"name":'First name must have more than one character'})

    if len(data['password']) < 7:
        raise({'password':'Password must be atleast 7 characters'})

    user = Users(**data)
    db.session.add(user)
    db.session.commit()

    return Userschema.dump(user),201
    
@app.route('/',methods=['GET','POST'])
@token_req
def home(current_user):     
    userdetail = Users.query.get(current_user.id)
    return {'WELCOME':userdetail.name}

@app.route('/database')
def database():
    db.create_all()
    cps = generate_password_hash('asdwrd')
    Admin = Users(name='Admine',username='Aswd',email = 'asdw@gmail.com',_password = cps)
    db.session.add(Admin)
    db.session.commit() 
    return {'Database':'Database created Sucessfully with an Admin'}


if __name__ == '__main__':
    app.run(debug = True)   