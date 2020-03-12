from flask import Flask, request, redirect, render_template, jsonify
from pymongo import MongoClient
from bson import json_util
import requests

app = Flask(__name__)

client = MongoClient()
db = client["APIIT"]
collection = db.to_dos

@app.route('/')
def index():
    user = {'username': 'Thilina'}
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/single-blog')
def single_blog():
    return render_template('single-blog.html')

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/fb')
def fb():
    return render_template('fb.html')


@app.route('/view', methods=['GET'])
def get_todos():
    to_dos = list(collection.find())
    return json_util.dumps(to_dos)

@app.route('/search')

def search():

    recipe = request.args.get('a', 0, type=str)

    response = requests.get(f"https://searchly.asuarez.dev/api/v1/song/search?query={recipe}")

    try:
        response = response.json()["response"]["results"][0]
    except:
        response = {"name": "Invalid search. Please try again."}
    return jsonify(result=response) 




@app.route('/add', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        new_todo = request.get_json()
        name = new_todo['name']
        description = new_todo['description']
        timer = new_todo['timer']

        collection.insert_one({
            "name": name,
            "description": description,
            "timer": timer
        })

    return redirect('/view')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
