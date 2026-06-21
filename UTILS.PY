import json 
from datetime import date


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


#Function to save sessions data to track progress
def save_sessions(total, correct, app):
    if total<10:
        return
    file_name = "data/sessions.json"
    current_entry = {"words_practiced":total,
                     "correct":correct,
                     "app":app,
                     "date": str(date.today())
                     } 
    
    saved_sessions = load_data(file_name)

    # To upate and save the current session
    for session in saved_sessions:
        if session["date"] == str(date.today()):
            index = saved_sessions.index(session)
            current_entry["words_practiced"] += session["words_practiced"]
            current_entry["correct"] += session["correct"]
            saved_sessions[index] = current_entry
            save_data(saved_sessions, file_name)
            return
    
    saved_sessions.append(current_entry)
    save_data(saved_sessions, file_name)


#To test utils.py
if __name__ == "__main__":
    data = load_data("data/spelling.json")
    print(data)  

                                  



    
    

    



