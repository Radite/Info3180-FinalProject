from flask import Flask, session
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import views dynamically
views_dir = os.path.join(os.path.dirname(__file__), 'views')
for filename in os.listdir(views_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]  # Remove '.py' extension
        module = __import__(f'app.views.{module_name}', fromlist=['*'])


from app import models



