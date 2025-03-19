from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Module docstring explaining the purpose of the file
"""
This file defines a Flask app with CRUD operations for managing resources in a database.
The operations include creating, reading, updating, and deleting resources.
"""

# Create and configure the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Resource(db.Model):
    """
    Class that represents resources in the database.
    Attributes:
        resource_id (int): The primary key for the resource.
        name (str): The name of the resource.
        quantity (int): The quantity of the resource.
    """

    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Resource object.
        """
        return f"<Resource {self.name}, Quantity: {self.quantity}>"

    def get_resource_details(self):
        """
        Returns a dictionary with the resource details.
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
    Returns a greeting message.
    """
    return "Hello, Mars Mission!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    """
    Adds a new resource to the database.
    Expects a JSON payload with the name and quantity of the resource.
    Returns a success message upon adding the resource.
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
    Returns a list of all resources in JSON format.
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
    Updates an existing resource in the database.
    Expects a JSON payload with updated name and quantity.
    Returns a success message if the resource is updated, or an error message if not found.
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
    Deletes a resource from the database.
    Returns a success message if the resource is deleted, or an error message if not found.
    """
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
