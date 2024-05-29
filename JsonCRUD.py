import json
import os

class JsonCRUD:
    def __init__(self, filename):
        self.filename = filename

    def is_empty(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return len(data['intents']) == 0
        except (FileNotFoundError, json.JSONDecodeError):
            return True

    def create_json_file(self):
        with open(self.filename, 'w') as file:
            json.dump({"intents": []}, file)

    def read_json(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"intents": []}
        return data

    def write_json(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create(self, tag, patterns, responses):
        if self.is_empty():
            self.create_json_file()
        data = self.read_json()
        data['intents'].append({"tag": tag, "patterns": patterns, "responses": responses})
        self.write_json(data)

    def read(self, tag):
        data = self.read_json()
        for item in data['intents']:
            if item['tag'] == tag:
                return item
        return None

    def Override(self, tag, new_patterns, new_responses):
        data = self.read_json()
        for item in data['intents']:
            if item['tag'] == tag:
                item['patterns'] = new_patterns
                item['responses'] = new_responses
                break
        self.write_json(data)

    def delete(self, tag):
        data = self.read_json()
        data['intents'] = [item for item in data['intents'] if item['tag'] != tag]
        self.write_json(data)
        
    def update(self, tag, new_patterns, new_responses):
        data = self.read_json()
        for item in data['intents']:
            if item['tag'] == tag:
                item['patterns'].extend(new_patterns)
                item['responses'].extend(new_responses)
                break
        self.write_json(data)



