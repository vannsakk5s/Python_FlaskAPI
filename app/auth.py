from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing credentials"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User signed up successfully!"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get('username')).first()

    if user and bcrypt.check_password_hash(user.password, data.get('password')):
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token, "token_type": "Bearer"}), 200

    return jsonify({"error": "Invalid username or password"}), 401