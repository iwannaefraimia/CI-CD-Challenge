from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # ✅ Το app ορίζεται μόνο μία φορά
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home route (test)
@app.route("/")
def home():
    return "Hello, Mars Mission!"

# CREATE - Add a new resource
@app.route('/resources', methods=['POST'])
def add_resource():
    data = request.json
    new_resource = Resource(name=data['name'], quantity=data['quantity'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added!"}), 201

# READ - Get all resources
@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    resource_list = [{"id": r.id, "name": r.name, "quantity": r.quantity} for r in resources]
    return jsonify(resource_list)

# UPDATE - Modify a resource
@app.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    data = request.json
    resource.name = data['name']
    resource.quantity = data['quantity']
    db.session.commit()
    return jsonify({"message": "Resource updated!"})

# DELETE - Remove a resource
@app.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == '__main__':
    app.run(debug=True)

