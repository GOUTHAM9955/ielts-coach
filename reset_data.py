import utils

# To hard reset spelling.json
def reset_spelling_stats():
    spellings_data = utils.load_data ("data/spelling.json")

    # Reset attempts, correct count and last_seen values
    for spelling in spellings_data:
        spelling["attempts"]=0
        spelling["correct"]=0
        spelling["last_seen"]=""
    
    utils.save_data(spellings_data, "data/spelling.json")
     


#To hard reset session.json file
def reset_session_stats():

    #Load the ssession data
    sessions_data = utils.load_data("data/sessions.json")

    #To reset last session or all the sessions
    print("Enter 1) For latest session")
    print("Enter 2) For all the sessions")

    option = input("Enter your choice -> ")

    # If used choose to delete latest sessions data
    if (option == "1"):
        if(len(sessions_data) == 0):
            print("No session data is available")
        else:
            utils.save_data(sessions_data[:-1],"data/sessions.json")
            print("Last sessions data is cleared")

    # If user choose to delete all sessions data
    elif(option == "2"):
        utils.save_data([],"data/sessions.json")
        print("All sessions data is wiped out")

    else:
        print ("It isn't a valid input")

if __name__ == "__main__":
    reset_spelling_stats()
    reset_session_stats()