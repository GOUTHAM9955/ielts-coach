import json 
import os


#Read a JSON file and returns it contents as python list
def load_data(filepath):
    #Try to open the file path
    try:
        with open(filepath) as file:
            return json.load(file)
    #If the file path doesn't exists or if we are unable to open
    except:
        return []
    
#To save data to a file
def save_data (data, filepath):
    #Try saving the data
    try:
        with open(filepath, "w") as file:
            #Code to save save data to file
            json.dump(data, file)
    except:
        print("Unable to update the file")

#To test utils.py
if __name__ == "__main__":
    data = load_data("data/spelling.json")
    print(data)


