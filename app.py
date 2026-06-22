from flask import Flask, render_template, request, redirect, url_for, session, send_file
import utils
import import_excel
import random
import os
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

    is_correct = spelling_quiz.check_answer_silent(user_answer, correct_word)

    session["total"] = session.get("total",0) + 1
    if is_correct:
        session["correct"] = session.get("correct",0) + 1
    
    return render_template("result.html", is_correct = is_correct, correct_word =correct_word)


# Shows the final score when user ends the quiz
@app.route("/spelling/end_quiz")
def end_quiz():
    total = session.get("total",0)
    correct = session.get("correct",0)
    session.clear()
    return render_template("end.html", total=total, correct=correct)




if __name__ == "__main__":
    app.run(debug=True)