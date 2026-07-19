from flask import Flask, render_template, request, redirect, url_for, session, send_file
import utils
import import_excel
import random
import os
from datetime import datetime
import spelling as spelling_quiz
from dotenv import load_dotenv

# Load .env file 
load_dotenv()

#To create a flask application
app = Flask(__name__)

#SESSION_ENCRIPTION_SECRET_KEY 
app.secret_key = os.getenv("SESSION_ENCRIPTION_SECRET_KEY")

# Home route function
@app.route("/")
def home():
    return render_template("home.html")

# Spelling quiz start page
@app.route("/spelling")
def spelling():
    return render_template("spelling.html")

#Loads a random word and shows it to the user
@app.route("/spelling/quiz")
def quiz():
    mode = request.args.get("mode")
    session["mode"] = mode
    session["total"] = session.get("total",0)
    session["correct"] = session.get("correct",0)
    if "start_time" not in session:
        session["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    words = utils.load_data("data/spelling.json")
    weights = spelling_quiz.get_weights(words)
    entry = random.choices(words, weights=weights, k=1)[0]
    session["word"] = entry["word"]

    return render_template("quiz.html", entry=entry, mode=mode)

# Checks user anser and checks if it is correct or wrong
@app.route("/spelling/check", methods=["POST"])
def check():
    user_answer = request.form.get("answer")
    correct_word = session.get("word")
    mode = session.get("mode")
    session["total"] = session.get("total",0) + 1

    # Check if the answer is right
    is_correct = spelling_quiz.check_answer_silent(user_answer, correct_word)


    # To load spelling.jsonn 
    spellings = utils.load_data("data/spelling.json")

    #To find the current word in the list of current words 
    for index, word_list in enumerate(spellings):
        if word_list["word"] == correct_word:
            word_index = index
            break
    
    # To update and save the spellings file
    spelling_quiz.update_word(spellings,word_index, is_correct)
    utils.save_data(spellings,"data/spelling.json")
    
    print(dict(session))
    return render_template("result.html", is_correct = is_correct, correct_word =correct_word)

# Route to clear the session data
@app.route("/spelling/clear_choice", methods=["POST"])
def clear_session():
    user_choice = request.form.get("choice")
    if user_choice == "current":
        sessions_data = utils.load_data("data/sessions.json")
        for index, session_list in enumerate(sessions_data):
            if session_list["start_time"] == session.get("start_time"):
                last_session_index = index
                break
        
        sessions_data.pop(last_session_index)
        utils.save_data(sessions_data,"data/sessions.json")

    if user_choice == "all":
        utils.save_data([],"data/sessions.json")
    
    session.clear()
    return redirect(url_for("home"))
        

# Shows the final score when user ends the quiz
@app.route("/spelling/end_quiz")
def end_quiz():
    total = session.get("total",0)
    correct = session.get("correct",0)
    start_time = session.get("start_time")
    utils.save_sessions(total, correct, start_time, "spelling")
    return render_template("end.html", total=total, correct=correct)

if __name__ == "__main__":
    app.run(debug=True)