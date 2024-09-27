from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data store
items = [
    {"id": 1, "name": "Item1", "category": "CategoryA", "available": True},
    {"id": 2, "name": "Item2", "category": "CategoryB", "available": False},
    # Add more items as needed
]

# 1. List All Items
@app.route('/items', methods=['GET'])
def list_all_items():
    return jsonify(items), 200

# 2. List Items by Name
@app.route('/items/name/<string:name>', methods=['GET'])
def list_items_by_name(name):
    filtered_items = [item for item in items if item['name'] == name]
    return jsonify(filtered_items), 200 if filtered_items else 404

# 3. List Items by Category
@app.route('/items/category/<string:category>', methods=['GET'])
def list_items_by_category(category):
    filtered_items = [item for item in items if item['category'] == category]
    return jsonify(filtered_items), 200 if filtered_items else 404

# 4. List Items by Availability
@app.route('/items/availability/<string:availability>', methods=['GET'])
def list_items_by_availability(availability):
    is_available = availability.lower() == 'true'
    filtered_items = [item for item in items if item['available'] == is_available]
    return jsonify(filtered_items), 200 if filtered_items else 404

# 5. Read Item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def read_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    return jsonify(item), 200 if item else 404

# 6. Update Item by ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    item.update(data)
    return jsonify(item), 200

# 7. Delete Item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
