import json

def repons():
    with open("respons.json", 'r') as file:
            res = json.load(file)
    return res["message"]

print(repons())
    