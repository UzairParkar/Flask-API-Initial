from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'apitest'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 

@app.route('/')
def Home():
    if 'username' in  session:
        username = session['username']
        return jsonify({'message':'You are already logged in','username': username})
    else:
        resp = jsonify({'messsage':'Unauthorized'})
        resp.status_code = 401
        return resp
    
@app.route('/signup',methods=['POST'])
def signup():
    json = request.json
    username = json['username']
    password = json['password']
    profession = json['profession']
    passhash = generate_password_hash(password)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO user (username,profession,password) VALUES (%s,%s,%s)"
    values = (username,profession,passhash)
    cursor.execute(sql,values)
    mysql.connection.commit()
    cursor.close()
    return "Signup Successful"

@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['username']
    _password = _json['password']
    print(_password)
    if _username and _password:       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         
        sql = "SELECT * FROM user WHERE username=%s"
        sql_where = (_username,)
         
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        username = row['username']
        password = row['password']
        if row:
            if check_password_hash(password, _password):
                session['username'] = username
                cursor.close()
                return jsonify({'message' : 'You are logged in successfully'})
            else:
                resp = jsonify({'message' : 'Bad Request - invalid password'})
                resp.status_code = 400
                return resp
        else:
            resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp







@app.route('/logout')
def logout():
    if 'username'in session:
        session.pop('username',None)
    return jsonify({'message':'You have logged Sucessfully Logged out'})


if __name__ == '__main__':
    app.run(debug=True)



