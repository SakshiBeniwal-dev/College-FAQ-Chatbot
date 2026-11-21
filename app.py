from flask import Flask, render_template, request, jsonify
import csv
import re
from difflib import SequenceMatcher

app = Flask(__name__)

# Read FAQ data

def load_faq():

    faqs = []

    with open("faq_data.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            faqs.append(row)

    return faqs


faq_data = load_faq()


# Clean text

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-z0-9\s]', '', text)

    return text


# Find answer

def find_answer(user_question):

    user_question = clean_text(user_question)

    best_match = None

    highest_score = 0

    user_words = set(user_question.split())

    for faq in faq_data:

        question = clean_text(faq["Question"])

        keywords = clean_text(faq["Keywords"])

        combined = question + " " + keywords

        faq_words = set(combined.split())

        common = user_words.intersection(faq_words)

        union = user_words.union(faq_words)

        word_score = len(common) / len(union) if union else 0

        similarity = SequenceMatcher(
            None, user_question, question
        ).ratio()

        score = (word_score * 0.6) + (similarity * 0.4)

        if score > highest_score:

            highest_score = score

            best_match = faq

    if highest_score >= 0.20 and best_match:

        return {
            "answer": best_match["Answer"],
            "category": best_match["Category"]
        }

    return {
        "answer": "Sorry, I couldn't understand your question. Please try asking differently or contact the college administration.",
        "category": "General"
    }


# Homepage

@app.route("/")
def home():

    return render_template("index.html")


# Chatbot response

@app.route("/get_response", methods=["POST"])
def get_response():

    user_message = request.json["message"]

    response = find_answer(user_message)

    return jsonify(response)


# Run application

if __name__ == "__main__":

    app.run(debug=True)