from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

'''
We will be visualising this api as created for a Notes application for better understanding and visualising
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/FSA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note_Display(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=True)
    desc = db.Column(db.String(900),nullable=False)
    ps = db.Column(db.String(200),nullable=True)
    dated = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return f'Note_Display(sno={self.sno}, title={self.title}, desc={self.desc}, ps={self.ps}, dated={self.dated})'

    def to_dict(self):
        return {
        'sno':self.sno,
        'title':self.title,
        'desc':self.desc,
        'dated':self.dated,
        'ps':self.ps}


with app.app_context():
    db.create_all()


@app.route('/',methods=['GET'])
def Home():
    Notes = Note_Display.query.all()
    for note in Notes:
        print(note.__repr__())
    return jsonify([note.to_dict() for note in Notes])

@app.route('/create',methods=['POST'])
def Create():
    data = request.get_json()
    Notes = Note_Display(title = data['title'],desc=data['desc'])
    db.session.add(Notes)
    db.session.commit()
    return jsonify(Notes.to_dict())


if __name__ == '__main__':
    app.run(debug=True)