import utils
import import_excel
import random
from colorama import Fore, Style, init
from gtts import gTTS
import os
from datetime import date
import time


#To initialize colorama for colorful texts
init()

#Function to play audio of a word using gTTS
def play_audio(word):

    #Check if the audio file already exists
    file_name = word.replace("/", "_").replace(" ", "_") + ".mp3"
    if os.path.exists("audio/"+file_name):
        os.system('afplay "audio/'+file_name + '"')
          
     
    else:
        #To convert text to audio and save the file
        tts = gTTS(text=word, lang="en")
        tts.save("audio/"+ file_name)

        #To play the audio file using terminal 
        os.system('afplay "audio/'+file_name + '"')
    
    time.sleep(3)

# This function validates if user entered spelling is correct
def check_answer(user_answer, correct):

    #Convert everythingto lower and remove spaces
    user_answer_lower = user_answer.lower().strip()
    correct_lower = correct.lower().strip()

    #Validation
    if user_answer_lower == correct_lower:
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
        print(Fore.GREEN + user_answer_lower.upper() + " is correct spelling")
        return True

    else:
        print(Fore.RED + "Correct spelling is: " + correct_lower.upper())
        print(Fore.RED + "Wrong!" + Style.RESET_ALL)
        return False

# Silent version of check_answer for web use - returns True or False without printing
def check_answer_silent(user_answer, correct):
    user_answer_lower = user_answer.lower().strip()
    correct_lower = correct.lower().strip()
    if user_answer_lower == correct_lower:
        return True
    else:
        return False


# To update the words status in json file
def update_word(words,index,is_correct):

    words[index]["attempts"] += 1

    if is_correct:
        words[index]["correct"] += 1

    words[index]["last_seen"] = str(date.today())

# Logic to process user chose
def user_choice(counter):
    # Counter for fixed retries
    counter += 1
    if counter == 4:
        return "0"
    #Login for quiz_type
    print("Enter 1) For audio test")
    print("Enter 2) For written test")
    option = input("Enter your choice here -> ")
    if(option == "1" or option == "2" ):
        return option
    else:
        print("Enter a valid option: " + str(4-counter) +" chances left")
        return user_choice(counter)
    
#Claculating weights for words list so that we words with frequent errors will get more weightage
def get_weights(words):
    list_weights = []
    for word in words:
        if word["attempts"] == 0:
            weight = 10
        else:
            weight = max(4, 10 - (word["correct"] / word["attempts"] * 10))
        list_weights.append(weight)
    return list_weights

                
            


#Main function to run the spelling test
def run_quiz():

    #To load words from Json
    words = utils.load_data("data/spelling.json")

    if len(words) == 0:
            imported_word_count = import_excel.import_spelling_words("credentials.json")
            if imported_word_count == 0:
                print("No words found to run the quiz! Please update the Vocabulary Googlesheets")
                return
            words = utils.load_data("data/spelling.json")
    
    #Prompting to user choice for quiz type
    print("Welcome to Spelling Practise!")
    quiz_option = user_choice(0)
    
    if(quiz_option == "0"):
        print("Exceeded maximum retries")
        exit()    

    total = 0
    correct_count = 0
    while(True):
        #For audio style quiz
        if(quiz_option == "1"):

            # To slect a random word for quiz until user is done with the quiz based on the calculated weights
            weights = get_weights(words)
            entry = random.choices(words, weights=weights, k=1)[0]
            random_index = words.index(entry)

            word = words[random_index]["word"]
            play_audio(word)
            user_entered_spelling = input("Enter your spelling here - > ")
            total +=1

            #Check the user input and update the spelling json accordingly
            if (check_answer(user_entered_spelling,word)):
                correct_count+=1
                update_word(words, random_index,True)
                utils.save_data(words, "data/spelling.json")
            else:
                update_word(words, random_index,False)
                utils.save_data(words, "data/spelling.json")

            #To check if user wishes to continue 
            again = input("Practice another word? (y to continue, any key to quit): ")
            if again.lower() != "y":
                break


        else:
            #For text style quiz

            # To slect a random word for quiz until user is done with the quiz based on the calculated weights
            weights = get_weights(words)
            entry = random.choices(words, weights=weights, k=1)[0]
            random_index = words.index(entry)

            word = words[random_index]["word"]
            print("Here is the word we need to correct: "+ words[random_index]["wrong"])
            user_entered_spelling = input("Enter your spelling here - > ")
            total +=1

            #Check the user input and update the spelling json accordingly
            if (check_answer(user_entered_spelling,word)):
                correct_count +=1
                update_word(words, random_index,True)
                utils.save_data(words, "data/spelling.json")

            else:
                update_word(words, random_index,False)
                utils.save_data(words, "data/spelling.json")

            #To check if user wishes to continue 
            again = input("Practice another word? (y to continue, any key to quit): ")
            if again.lower() != "y":
                break
        
    
    print("Session complete!")
    print("Words practiced: " +str(total))
    print("Correct: " +str(correct_count))
    if total > 0:
        print("Score: " + str(round(correct_count/total * 100)) + "%")
    else:
        print("No words practiced.")

    # To save the sessions data for progress tracking when more than 10 words are practised
    utils.save_sessions(total, correct_count, "spelling")


if __name__ == "__main__":
    run_quiz()






