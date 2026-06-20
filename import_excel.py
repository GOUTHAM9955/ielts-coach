import gspread
from google.oauth2.service_account import Credentials
import json
import utils

#Function to read lexical error data from excel file, cleanse and transform it to JSON format
def import_spelling_words(file_path):
    #Define google api permission
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # To create credential object that google accepts
    creds = Credentials.from_service_account_file(file_path, scopes= scopes)

    #Connect to google sheets
    client = gspread.authorize(creds)

    #To open lexical error google worksheet  
    sheet = client.open("Vocabulary")
    worksheet = sheet.worksheet("lexical error")

    #Read data from worksheet
    rows = worksheet.col_values(1)

    # List to store words from worksheets
    words = []
    for row in rows:
        #If row is empty skip it
        if row =="":
            continue
        
        #split the word based on → and rwmove extra spaces
        parts = row.split("→")
        wrong =parts[0].strip()
        correct = parts[1].strip()

        #Dictionary to store words matching JSON format
        entry ={
            "word":correct,
            "wrong":wrong,
            "attempts":0,
            "correct":0,
            "last_seen":""
        }

        words.append(entry)
    
    # Save words to spelling.json and return count
    utils.save_data(words, "data/spelling.json")
    return len(words)

if __name__ == "__main__":
    words_imported = import_spelling_words("credentials.json")
    print("words imported from worksheet are: " + str(words_imported))
    
















