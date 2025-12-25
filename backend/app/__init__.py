from flask import Flask

def create_app():
    app = Flask(__name__)

    # register NLP routes
    from app.nlp.nlp_routes import nlp_bp
    app.register_blueprint(nlp_bp)

    return app
# app/__init__.py

