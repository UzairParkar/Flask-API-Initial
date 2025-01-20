from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import csv
from werkzeug.utils import secure_filename
import io
import openpyxl


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/freccrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Students(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name  = db.Column(db.String(30))
    rollno = db.Column(db.Integer,unique=True)
    std = db.Column(db.String(10))
    course = db.Column(db.String(20))


    def __init__(self,name,rollno,std,course):
        self.name = name
        self.rollno = rollno
        self.std = std
        self.course = course

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('name','rollno','std','course')


PostStudent = StudentSchema()
PostsStudent = StudentSchema(many = True)


with app.app_context():
    db.create_all()

with app.app_context():
    dbRollno = Students.query.with_entities(Students.rollno).all()
    existing = [roll[0] for roll in dbRollno] 


@app.route('/csvUpload', methods=['POST'])
def csvUpload():
    if request.files:
        uploaded_file = request.files['filename']
        data = uploaded_file.stream.read()
        stream = io.StringIO(data.decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        i=0
        for row in reader:
            i+=1
            if i==1:
                continue
            else:
                if int(row[1]) in existing:
                    name = row[0]
                    std = row[2]
                    course = row[3]
                    col = Students.query.filter_by(rollno=row[1]).first()
                    if col.name!=name or col.std!=std or col.course!=course:
                        col.name=name
                        col.std=std
                        col.course=course
                        db.session.add(col) 
                    else:
                        continue
                else:
                    my_posts=Students(*row)
                    db.session.add(my_posts)
                    
        db.session.commit()
    return jsonify({'message' : 'csv file successfully uploaded'})


@app.route('/excelUpload',methods=['POST'])
def excelUpload():
    if request.files:
        uploaded_file = request.files['filename']
        wb_obj=openpyxl.load_workbook(uploaded_file)
        sheet=wb_obj.active
        l=0
        for row in sheet.values:
            l+=1
            if l==1:
                continue
            else:
                if row[1] in existing:
                    name = row[0]
                    std = row[2]
                    course = row[3]
                    col = Students.query.filter_by(rollno=row[1]).first()
                    if col.name!=name or col.std!=std or col.course!=course:    
                        col.name=name
                        col.std=std
                        col.course=course
                        db.session.add(col)
                    else:
                        continue
                else:
                    my_posts=Students(*row)
                    db.session.add(my_posts)

        db.session.commit()
    return jsonify({'message' : 'Excel File successfully uploaded'})


@app.route("/get", methods=["GET"])
def get_post():
    details=Students.query.all()
    result=PostsStudent.dump(details) 
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)