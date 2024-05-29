from JNodeDB import JNodeDB
import pandas as pd






# FoodTable.createEntry(0, {
#         "Name": "Espresso",
#         "Price": 3.5,
#         "Qty": 50,
#         "Type": "Coffee"
#         })

# FoodTable.createEntry(1,{
#             "Name": "Latte",
#             "Price": 4.5,
#             "Qty": 40,
#             "Type": "Coffee"
#         })


# FoodTable.createEntry(2,{
#         "Name": "Cappuccino",
#         "Price": 4,
#         "Qty": 35,
#         "Type": "Coffee"
#     })
            
# FoodTable.createEntry(3,{
#             "Name": "Croissant",
#             "Price": 2.5,
#             "Qty": 25,
#             "Type": "Pastry"
#         })

# FoodTable.createEntry(4,{
#             "Name": "Muffin",
#             "Price": 3,
#             "Qty": 20,
#             "Type": "Pastry"
#         })
            
# FoodTable.createEntry(5, {
#         "Name": "Americano",
#         "Price": 3.75,
#         "Qty": 45,
#         "Type": "Coffee"
#     })



FoodTable = JNodeDB("FoodTable")

def FoodMenu():

    fooddata = FoodTable.readJson()

    print(pd.DataFrame.from_dict(fooddata, orient='index'))

  
FoodMenu()

    



