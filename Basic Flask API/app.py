from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home_page():
    return '<h1>Hello World</h2>\n<p>Restful API Creation</p>'




@app.route('/checkage/<int:age>')
def check_age(age):
    if age < 18:
        result = {
            'age':age,
            'eligible':False,
            'TokenNo':18.21
        }
        print(result)
    else:
        result = {
            'age':age,
            'eligible':True,
            'TokenNo':18.22
        }
        print(result)

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True) 