from flask import Flask
from .database.db import db
import os


# from routes.admin import admin
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)

# # db=SQLAlchemy()
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)
with app.app_context():
    print("KDJHJHD")
    db.create_all()
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


#register blueprints
# app.register_blueprint(admin.admin)