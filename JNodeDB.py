
import os
import json

class JNodeDB:
    def __init__(self,Node):
        # Initialize the JSON file if it does not exist
        self.Node = Node
        if not os.path.exists(self.getCurrent_working_directory(Node)):
            with open(self.getCurrent_working_directory(Node), 'w') as file:
                json.dump({}, file)
    
    def getCurrent_working_directory(self,Node):
        # Get the current working directory
        return os.getcwd()+"\\"+Node+".json"


    def readJson(self):
        if not os.path.exists(self.getCurrent_working_directory(self.Node)):
            with open(self.getCurrent_working_directory(self.Node), 'w') as file:
                json.dump({}, file)
        """Read data from the JSON file."""
        with open(self.getCurrent_working_directory(self.Node), 'r') as file:
            return json.load(file)
    
    def writeJson(self,data):
        """Write data to the JSON file."""
        with open(self.getCurrent_working_directory(self.Node), 'w') as file:
            json.dump(data, file, indent=4)

    def createEntry(self,key, value):
        """Create a new entry in the JSON file."""
        data = self.readJson()
        if key in data:
            raise KeyError(f"Key '{key}' already exists.")
        data[key] = value
        self.writeJson(data)
        print(f"Entry '{key}' created.")

    def readEntry(self,key):
        """Read an entry from the JSON file."""
        data = self.readJson()
        if(data != None):
            return data
        raise KeyError(key, f"Key '{key}' not found.")

    def updateEntry(self,key, value):
        """Update an existing entry in the JSON file."""
        data = self.readEntry(key)
        data[key] =value
        self.writeJson(data)
        print(f"Entry '{key}' updated.")

    def delete_entry(self,key):
        """Delete an entry from the JSON file."""
        data = self.readEntry(key)
        del data[key]
        self.writeJson(data)
        print(f"Entry '{key}' deleted.")

    def listEntries(self):
        """List all entries in the JSON file."""
        data = self.readJson()
        return data



