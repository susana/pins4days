from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify


app = Flask(__name__)


@app.route('/auth', methods=['POST'])
def initial_auth():
    print("hi")
    if request.method == 'POST':
        json = request.get_json()
        challenge = json['challenge']
        return jsonify(challenge=challenge)
