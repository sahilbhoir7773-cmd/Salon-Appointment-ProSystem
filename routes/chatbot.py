from flask import Blueprint, render_template

chatbot = Blueprint("chatbot", __name__)

@chatbot.route("/chat")
def chat():
    return render_template("chatbot.html")