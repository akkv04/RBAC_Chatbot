from flask import Flask, render_template, request
from engine.intent_engine import classify_intent
from engine.qa_engine import get_answer
from engine.rule_engine import diagnose

app = Flask(__name__)

def process_query(query):
    intent = classify_intent(query)

    diagnosis = diagnose(query)
    if diagnosis:
        return intent, "⚠ Possible Causes:\n- " + "\n- ".join(diagnosis)

    answer = get_answer(query)
    if answer:
        return intent, answer

    return intent, "❌ No match found. Try rephrasing."


@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    intent = ""

    if request.method == "POST":
        query = request.form["query"]
        intent, response = process_query(query)

    return render_template("index.html", response=response, intent=intent)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)