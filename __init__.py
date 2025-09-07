# animal_bird_kb_ui/__init__.py

# Import the Flask app
from .app import app

# Import routes to register them with Flask app
from .routes import animal_routes

# Optional: import any utilities or models if you want them available at package level
from .models import animals
from .utils import score_calculator

# This allows users to do:
# from animal_kb_ui import app, animals, score_calculator

