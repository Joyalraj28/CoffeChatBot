from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

import random

from reply import reply


app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)


api = Api(app)

class Items(Resource):
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
            return {'message':  reply(message)},
        except Exception  as e:
            return {'message': e.args}, 404
         
api.add_resource(Items, '/')

if __name__ == '__main__':
    app.run(debug=True)