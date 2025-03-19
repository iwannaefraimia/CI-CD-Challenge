from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Resource(db.Model):
    """
    Κλάση που αναπαριστά τους πόρους στην βάση δεδομένων.
    """
    resource_id = db.Column(db.Integer, primary_key=True)  # Αλλαγή από 'id' σε 'resource_id'
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home route (test)
@app.route("/")
def home():
    """
    Απλή διαδρομή που επιστρέφει ένα μήνυμα καλωσορίσματος.
    """
    return "Hello, Mars Mission!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    """
    Προσθέτει έναν νέο πόρο στην βάση δεδομένων.
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
    Επιστρέφει όλους τους πόρους από τη βάση δεδομένων.
    """
    resources = Resource.query.all()
    resource_list = [{"resource_id": r.resource_id, "name": r.name, "quantity": r.quantity} for r in resources]
    return jsonify(resource_list)

# UPDATE - Modify a resource
@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """
    Τροποποιεί έναν πόρο με βάση το id του.
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
    Διαγράφει έναν πόρο με βάση το id του.
    """
    resource = Resource.query.get(resource_id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
