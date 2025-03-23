"""main Flask application
It provides CRUD operations to manage resources in the db"""
import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Create and configure the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model - resource with attributes like name and quantity
class Resource(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Resource {self.name}, Quantity: {self.quantity}>"

    def get_resource_details(self):
        return {"name": self.name, "quantity": self.quantity}

# tables in the db
with app.app_context():
    db.create_all()

# Home route to check if the Flask app is running
@app.route("/")
def home():
    return "Mars Mission Application Running!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    data = request.json # Expects a JSON payload with the name and quantity of the resource
    new_resource = Resource(name=data['name'], quantity=data['quantity'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added!"}), 201

# READ - Get all resources from db
@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    resource_list = [
        {"resource_id": r.resource_id, "name": r.name, "quantity": r.quantity}
        for r in resources
    ]
    return jsonify(resource_list)

# UPDATE - Modify an existing resource in the db
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    data = request.json
    resource.name = data['name']
    resource.quantity = data['quantity']
    db.session.commit()
    return jsonify({"message": "Resource updated!"}) # Expects a JSON payload with the updated name and quantity

# DELETE - Remove a resource from db
@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
