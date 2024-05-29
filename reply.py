import random
import json
import torch
from model import NeuralNet
from spacy_utils import bag_of_words, tokenize
from order import order
import nltk
from nltk.corpus import wordnet
from JNodeDB import JNodeDB
import pandas as pd

# nltk.download('wordnet')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

#Not Understand Collection
NotUnderstandCollection = JNodeDB("NotUnderstandCollection")
#Food Table
FoodTable = JNodeDB("FoodTable")


model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()



def reply(response):
    sentence = tokenize(response)
                                                                    
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    #List of items
    tag = tags[predicted.item()]
   
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response =  random.choice(intent['responses'])
                if tag == "menu":
                    fooddata = FoodTable.readJson()
                    menudata = pd.DataFrame.from_dict(fooddata, orient='index')
                    return response+menudata
                elif str(response).strip() == "asking_prices":
                    return None
                elif str(response).strip() == "giving_order":
                    response = order(response)
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
                
reply("Which items do you have?")

   
    