from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json

import random

def repons():
    with open("respons.json", 'r') as file:
            res = json.load(file)
    return res["message"]
    


app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)


api = Api(app)

class ChatBot(Resource):
    def __init__(self):
        super().__init__()
    def get(self):
        try:
            # Convert dictionary values to a list and choose one randomly
            messages = list()
            if messages:  # Check if the list is not empty
              message = random.choice(messages)
              return message
            else:
              return {'message': 'No messages available'}, 404
        except:
            return {'message': 'No messages available'}, 404
        
    def post(self):
        try:
           
            data = request.get_json()
            message = data['message']
            return {'message':  repons()},
        except Exception  as e:
            return {'message': e.args}, 404
         
api.add_resource(ChatBot, '/')

if __name__ == '__main__':
    app.run(debug=True)