from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import csv
from werkzeug.utils import secure_filename  
import io
import openpyxl
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ferapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    std = db.Column(db.Integer,nullable=False)
    course = db.Column(db.String(40),nullable=False)
    date_joined = db.Column(db.DateTime,default = datetime.utcnow)

    def __init__(self,name,std,course):
        self.name = name
        self.std = std
        self.course = course

    def __repr__(self):
        return self.name


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id','name','std','course','date_joined')

studentSchema = StudentSchema()
studentsSchema = StudentSchema(many=True)

with app.app_context():
    db.create_all()

@app.route('/excelupload',methods=['POST'])
def ExcelUpload():
    if request.files:
        file = request.files['filename']
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        i = 0 
        for row in sheet.values:
            i +=1
            if i == 1:
                continue
            else:
                mystudent=Student(*row)
                db.session.add(mystudent)
        db.session.commit()
        return jsonify({'message':'Excel File sucessfully uploaded'}),201



@app.route('/students',methods=['GET'])
def get_students():
    all_students = Student.query.all()
    return studentsSchema.jsonify(all_students)




@app.route('/uploadcsv',methods=['POST'])
def Upload_CSV():
    if request.files:
        uploaded_file = request.files['filename']
        data = uploaded_file.stream.read()
        stream = io.StringIO(data.decode("UTF8"),newline=None)
        reader = csv.reader(stream)
        i = 0
        for row in reader:
            print(row)
            i+=1
            if i == 1:
                continue
            else:
                myposts=Student(*row)
                db.session.add(myposts)
                
                
                
        db.session.commit()
        return jsonify({'Message':"CSV file Sucessfully uploaded"})






@app.route('/data',methods=['POST'])
def data():
    file = request.files['data']
    stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
    readit = csv.reader(stream)
    
    for row in readit:
        print('Row:', row)

    return jsonify({'message': 'File successfully uploaded'})

if __name__ == '__main__':
    app.run(debug=True)