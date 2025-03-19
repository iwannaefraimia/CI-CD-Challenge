from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Module docstring explaining the purpose of the file
"""
This file defines a Flask app with CRUD operations for managing resources.
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
    """
    resource_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id' to 'resource_id'
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """ Returns the string representation of the resource for easier management """
        return f"<Resource {self.name}, Quantity: {self.quantity}>"

    # Example additional method to avoid "too few public methods" warning
    def get_resource_details(self):
        """ Returns a dictionary of resource details """
        return {"name": self.name, "quantity": self.quantity}

# Create tables in the database
with app.app_context():
    db.create_all()

# Home route (test)
@app.route("/")
def home():
    """
    Simple route that returns a welcome message.
    """
    return "Hello, Mars Mission!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    """
    Adds a new resource to the database.
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
    Returns all resources from the database.
    """
    resources = Resource.query.all()
    resource_list = [{"resource_id": r.resource_id, "name": r.name, "quantity": r.quantity} for r in resources]
    return jsonify(resource_list)

# UPDATE - Modify a resource
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """
    Modifies a resource based on its id.
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
    Deletes a resource based on its id.
    """
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
