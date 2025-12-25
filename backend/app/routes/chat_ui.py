from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)

@ui_bp.route("/chat")
def chat():
    return render_template("chat.html")
