from flask_sqlalchemy import SQLAlchemy
from app import app

# Configure the PostgreSQL Database Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/databaseName'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
