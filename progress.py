import utils
import matplotlib.pyplot as plt

#To visualize word accuracy
def show_word_accuracy():
    words = utils.load_data("data/spelling.json")

    # To track the words we practiced
    practiced = []
    for word in words:
        if word["attempts"] > 0:
            practiced.append(word)
    
    labels = []
    scores = []

    #To extract labels and calculate their scores
    for entry in practiced:
        word = entry["word"]
        score = round(entry["correct"]/entry["attempts"] * 100)
        labels.append(word)
        scores.append(score)
    # Plot size
    plt.figure(figsize=(12,6))
    # Graph style
    plt.bar(labels,scores)
    #To rotate lables so that it wont overlap
    plt.xticks(rotation = 45)
    # labels the Y axis
    plt.ylabel("Accuracy %")
    # adds a title
    plt.title("Word Accuracy")
    # prevents labels from being cut off
    plt.tight_layout() 
    #display the chart
    plt.show()

# Function to show progress over time
def show_progress_over_time():
    session_data = utils.load_data("data/sessions.json")

    date = []
    scores = []
    for session in session_data:
        if session["app"] == "spelling":
            session_date = session["date"]
            score = round(session["correct"]/session["words_practiced"] * 100)
            date.append(session_date)
            scores.append(score)
    
    #plot size
    plt.figure(figsize=(12,6))
    #Graph style
    plt.plot(date, scores, marker="o", color="green")
    #To rotate lables so that it wont overlap
    plt.xticks(rotation=45, ha="right")
    # labels the Y axis
    plt.ylabel("Score %")
    # adds a title
    plt.title("Spelling Progress Over Time")
    # prevents labels from being cut off
    plt.tight_layout() 
    #display the chart
    plt.show()



if __name__ == "__main__":
    show_word_accuracy()
    show_progress_over_time()