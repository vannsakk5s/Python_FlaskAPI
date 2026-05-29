from flask import Blueprint, request, jsonify
from app import db
from app.models import Item
from flask_jwt_extended import jwt_required

crud_bp = Blueprint('crud', __name__)

# 1. CREATE (POST)
@crud_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    new_item = Item(title=data['title'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created!"}), 201

# 2. READ ALL (GET)
@crud_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    output = [{"id": i.id, "title": i.title, "description": i.description} for i in items]
    return jsonify(output), 200

# 3. UPDATE (PUT)
@crud_bp.route('/items/<int:id>', methods=['PUT'])
@jwt_required()
def update_item(id):
    data = request.get_json()
    item = Item.query.get_or_404(id)
    item.title = data['title']
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({"message": "Item updated!"}), 200

# 4. DELETE (DELETE)
@crud_bp.route('/items/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted!"}), 200