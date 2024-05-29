import random
import json
import torch
from model import NeuralNet
from spacy_utils import bag_of_words, tokenize
# from nltk_utils import bag_of_words, tokenize
from items_list import items 
from order import order
from train import data
from JNodeDB import JNodeDB

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Not Understand Collection
NotUnderstandCollection = JNodeDB("NotUnderstandCollection")


with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# FILE = "data.pth"
# data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# print(input_size,hidden_size,output_size,all_words,tags,model_state)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

names = list(items.keys())
prices = list(items.values())
text = ""

History = {}

for item , price in items.items():
    text += f"""
    {item.upper()}  -----  {price} $. \n
    """
def reply(input):
    sentence = tokenize(input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print(prob.item())
    if prob.item() > 70:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                if str(response).strip() == "asking_menu":
                    return f"{text}"
                elif str(response).strip() == "asking_prices":
                    return f"{text}"
                elif str(response).strip() == "giving_order":
                    response = order(input)
                    return response
                else:
                    return response
    else:
        jsondis = NotUnderstandCollection.readJson()
        key = [i for i in jsondis if jsondis[i]['patterns'] == input]
        if key != None and len(key) > 0:
               count =  int(jsondis[key[0]]['RequestCount'])
               count+=1
               NotUnderstandCollection.updateEntry(key[0],{"patterns":input,"RequestCount":count})
               return "Sorry! Currently, I am trying to train to answer question"
               
        else:
            randomkey = random.randint(1, 1000)
            NotUnderstandCollection.createEntry(randomkey,{"patterns":input,"RequestCount":1})
            return "Sorry! I did not understand this."
            

reply('hi')