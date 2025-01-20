from flask import Flask, request, jsonify, redirect, Response
from datetime import datetime

app = Flask(__name__)
'''For better visualisation, we will assume that this Api 
is for a notes application'''


# db is your database in the form of a list  as your database 
db = []

# note_sr is your id
note_sr = 1

@app.route('/')
def Home_page():
    return 'Hello World',200

@app.route('/create',methods=['POST'])
def create_notes():
    global note_sr
    data = request.json
    current_date = datetime.now().strftime( "%d/%m/%Y, %H:%M:%S")
    note = {
        'sr':note_sr,
        'Title':data['Title'],
        'Note':data['Note'],
        'Date':current_date
    }
    note_sr += 1
    db.append(note)
    return jsonify(note),201

@app.route('/read',methods=['GET'])
def read_notes():
    return jsonify(db)

@app.route('/read/<int:note_sr>',methods=['GET'])
def read_by_id(note_sr):
    for fid in db:
        if fid['sr'] == note_sr:
            return jsonify(fid),201
    return jsonify({'message':'id not found'})

@app.route('/update/<int:note_sr>',methods=['PUT'])
def update_notes(note_sr):
    for fid in db:
        if fid['sr'] == note_sr:
            fid['Title'] = request.json.get('Title',fid['Title'])
            fid['Note'] = request.json.get('Note',fid['Note'])
            return jsonify(fid)
    return jsonify({"message":"Notes Not found"})

@app.route('/delete/<int:note_sr>',methods=['DELETE'])
def delete_notes(note_sr):
    for fid in db:
        if fid['sr'] ==note_sr:
            db.remove(fid)
            return ({'Message':'Notes Removed'})
    return ({'Message':'Notes Do not exist'})

if __name__ == '__main__':
    app.run(debug=True)

