from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Import routes (assuming routes are defined in app/routes.py)
from app import routes
