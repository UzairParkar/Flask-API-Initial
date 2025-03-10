from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///marsh15.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description= db.Column(db.String(200),nullable=True)
    author = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.title}'

    def __init__(self,title,description,author):
        self.title = title
        self.description = description
        self.author = author


class PostSchema(ma.Schema):
    class Meta:
        fields = ("title","author","description")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/')
def home():
    return 'Working'

@app.route('/addposts',methods=['POST'])
def add_posts():
    title = request.json['title']
    desc = request.json['description']
    author = request.json['author']
    my_posts = Post(title,desc,author) 
    db.session.add(my_posts)
    db.session.commit()

    return post_schema.jsonify(my_posts)


@app.route('/get',methods=['GET'])
def get_posts():
    all_posts=Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)

@app.route('/getbyid/<id>/',methods=['GET'])
def details_id(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)

@app.route('/update/<id>/',methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    
    post.title = title
    post.description = description
    post.author = author

    db.session.commit()
    return post_schema.jsonify(post)

@app.route('/delete/<id>',methods =['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)


if __name__ == '__main__':
    app.run(debug=True)