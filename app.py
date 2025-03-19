import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Module docstring explaining the purpose of the file
"""
This file defines a Flask application with CRUD operations to manage resources in a database.
The app allows adding, viewing, updating, and deleting resources.
"""

# Create and configure the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Resource(db.Model):
    """
    Represents a resource in the database.
    """
    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        Return a string representation of the Resource object.
        """
        return f"<Resource {self.name}, Quantity: {self.quantity}>"

    def get_resource_details(self):
        """
        Returns the details of the resource as a dictionary.
        """
        return {"name": self.name, "quantity": self.quantity}

# Create tables in the database
with app.app_context():
    db.create_all()

# Home route
@app.route("/")
def home():
    """
    A simple test route to check if the app is working.
    """
    return "Hello, Mars Mission!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    """
    Add a new resource to the database.
    Expects a JSON payload with the name and quantity of the resource.
    """
    data = request.json
    new_resource = Resource(name=data['name'], quantity=data['quantity'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added!"}), 201

# READ - Get all resources
@app.route('/resources', methods=['GET'])
def get_resources():
    """
    Retrieves all resources from the database.
    """
    resources = Resource.query.all()
    resource_list = [
        {"resource_id": r.resource_id, "name": r.name, "quantity": r.quantity}
        for r in resources
    ]
    return jsonify(resource_list)

# UPDATE - Modify a resource
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """
    Update an existing resource in the database.
    Expects a JSON payload with the updated name and quantity.
    """
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    data = request.json
    resource.name = data['name']
    resource.quantity = data['quantity']
    db.session.commit()
    return jsonify({"message": "Resource updated!"})

# DELETE - Remove a resource
@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Delete a resource from the database.
    """
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)