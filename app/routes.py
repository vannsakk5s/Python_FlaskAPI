from flask import Blueprint, request, jsonify
from app import db
from app.models import Product
from flask_jwt_extended import jwt_required

crud_bp = Blueprint('crud', __name__)


@crud_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json() or {}

    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400

    if data.get('price') is None:
        return jsonify({"error": "Price is required"}), 400

    if data.get('categoryId') is None:
        return jsonify({"error": "Category ID is required"}), 400

    new_product = Product(
        productImg=data.get('productImg'),
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        categoryId=data['categoryId']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "id": new_product.id
    }), 201


@crud_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()

    output = [
        {
            "id": p.id,
            "productImg": p.productImg,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "categoryId": p.categoryId
        }
        for p in products
    ]

    return jsonify(output), 200


@crud_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)

    return jsonify({
        "id": product.id,
        "productImg": product.productImg,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "categoryId": product.categoryId
    }), 200


@crud_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.get_json() or {}
    product = Product.query.get_or_404(product_id)

    product.productImg = data.get('productImg', product.productImg)
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.categoryId = data.get('categoryId', product.categoryId)

    db.session.commit()

    return jsonify({"message": "Product updated successfully"}), 200


@crud_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted from database"}), 200