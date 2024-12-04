from flask_sqlalchemy import SQLAlchemy
from app import app

# Configure the PostgreSQL Database Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass123@localhost:5432/Pearl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

