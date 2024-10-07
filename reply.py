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
import re

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
#Order table
OrderTable = JNodeDB("OrderTable")


model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def order(text):
    order = {}
    prices = []
    total = 0
    
    ordersjson = OrderTable.readJson()
    orderid = len(ordersjson.keys())+1

    selectitems = {}
    items = FoodTable.readJson()
    id = 1
    for i in items:
        search = re.findall(items[i]["Name"], text)
        for value in search:
            if value not in order:
                order[i] ={
                     "Name": items[i]["Name"],
                     "Price": items[i]["Price"],
                     "Qty": 1,
                     "Type": items[i]["Type"]
                }
                selectitems[id] = {
                   "Name": items[i]["Name"],
                   "Price":str(items[i]["Price"])+"/="
                }
                total += int(items[i]["Price"])
                id+=1
    if len(selectitems) > 0:
        OrderTable.createEntry(orderid,{"items":order,"Total":total})

        order_items =pd.DataFrame.from_dict(selectitems, orient='index')
        output = "ORDER PLACED.\n"+str(order_items)+"\nTotal : "+str(total)+"/="
    else:
        jsondis = NotUnderstandCollection.readJson()
        key = [i for i in jsondis if jsondis[i]['patterns'] == text]
        if key != None and len(key) > 0:
               count =  int(jsondis[key[0]]['RequestCount'])
               count+=1
               NotUnderstandCollection.updateEntry(key[0],{"patterns":text,"RequestCount":count})
        else:
            randomkey = random.randint(1, 1000)
            NotUnderstandCollection.createEntry(str(randomkey)+"_No_item_Found",{"patterns":text,"RequestCount":1})
        return "Sorry! currently this items not available.we are discussing about add this item in menu"
        
  
    return output



def askprice(text):
    
    selectitems = {}
    items = FoodTable.readJson()
    list =[]
    id = 1
    for i in items:
        search = re.findall(items[i]["Name"], text)
        for value in search:
            if value not in selectitems:
                list.append(items[i]["Name"])
                selectitems[id] = {
                   "Name": items[i]["Name"],
                   "Price":str(items[i]["Price"])+"/="
                }
                id+=1

    if len(list) > 0:
        data = ",".join(list)
        summary = "Price of "+data+"\n"+str(pd.DataFrame.from_dict(selectitems, orient='index'))
        return summary
    else:
        jsondis = NotUnderstandCollection.readJson()
        key = [i for i in jsondis if jsondis[i]['patterns'] == text]
        if key != None and len(key) > 0:
               count =  int(jsondis[key[0]]['RequestCount'])
               count+=1
               NotUnderstandCollection.updateEntry(key[0],{"patterns":text,"RequestCount":count})
        else:
            randomkey = random.randint(1, 1000)
            NotUnderstandCollection.createEntry(str(randomkey)+"_No_item_Found",{"patterns":text,"RequestCount":1})
        return "Sorry! currently this items not available.we are discussing about add this item in menu"
        
        



def reply(response):
    sentence = tokenize(response)
    text = response
                                                                    
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
                    return response+str(menudata)
                elif str(response).strip() == "asking_prices":
                    return askprice(text)
                elif str(response).strip() == "giving_order":
                    response = order(text)
                    return response
                else:
                    return response
    else:
        jsondis = NotUnderstandCollection.readJson()
        key = [i for i in jsondis if jsondis[i]['patterns'] == response]
        if key != None and len(key) > 0:
               count =  int(jsondis[key[0]]['RequestCount'])
               count+=1
               NotUnderstandCollection.updateEntry(key[0],{"patterns":response,"RequestCount":count})
               return "Sorry! I don't understand this question now. I am currently trying to understand this question."
        else:
            randomkey = random.randint(1, 1000)
            NotUnderstandCollection.createEntry(str(randomkey)+"_Not_UnderStand",{"patterns":response,"RequestCount":1})
            return "Sorry! I did not understand this."



# while True:
#     txt = input(">> ")
#     print(reply(txt))
   
    