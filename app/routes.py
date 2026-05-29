from flask import Blueprint, request, jsonify
from app import db
from app.models import Item
from flask_jwt_extended import jwt_required

crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json() or {}
    if not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    new_item = Item(title=data['title'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item created successfully", "id": new_item.id}), 201


@crud_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    output = [{"id": i.id, "title": i.title, "description": i.description} for i in items]
    return jsonify(output), 200


@crud_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    data = request.get_json() or {}
    item = Item.query.get_or_404(item_id)

    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({"message": "Item updated successfully"}), 200


@crud_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item dropped from database"}), 200