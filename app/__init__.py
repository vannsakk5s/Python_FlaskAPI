import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # configure database & JWT
    app.config['SQLALCHEMY_DATABASE_KEY'] = os.getenv('SQLALCHEMY_URL', 'postgresql://user:password@db:5432/flaskdb')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-khmer-key')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from app.auth import auth_bp
    from app.routes import crud_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(crud_bp)

    return  app