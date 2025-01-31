from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    dated= db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'{self.sno} | {self.title} | {self.desc} | {self.dated}\n'

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title'] 
        desc  = request.form['desc']
        todo = Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit() 
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo),200

@app.route('/delete/<int:sno>')
def delete_tasks(sno):
    TooDoo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(TooDoo)
    db.session.commit() 
    return redirect('/')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update_tasks(sno):
     if request.method == 'POST':
        title = request.form['title'] 
        desc  = request.form['desc']
        TooDoo = Todo.query.filter_by(sno=sno).first()
        TooDoo.title = title
        TooDoo.desc = desc
        db.session.add(TooDoo)
        db.session.commit()
        return redirect('/')
     TooDoo = Todo.query.filter_by(sno=sno).first()
     return render_template('update.html',TooDoo=TooDoo)
     
if __name__ == '__main__':
    app.run(debug=True,port=1900)