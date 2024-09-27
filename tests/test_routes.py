from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Sample in-memory database (replace with your actual database)
items = [
    {'id': 1, 'name': 'item1', 'category': 'category1', 'available': True},
    {'id': 2, 'name': 'item2', 'category': 'category2', 'available': False},
    # Add more items as needed
]

# Read: Get an item by ID
@app.route('/item/<int:item_id>', methods=['GET'])
def read(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        abort(404)
    return jsonify(item), 200

# Create: Add a new item (for completeness)
@app.route('/item', methods=['POST'])
def create():
    data = request.get_json()
    new_item = {
        'id': len(items) + 1,
        'name': data['name'],
        'category': data['category'],
        'available': data['available']
    }
    items.append(new_item)
    return jsonify(new_item), 201

# Update: Update an item by ID
@app.route('/item/<int:item_id>', methods=['PUT'])
def update(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        abort(404)

    data = request.get_json()
    item.update({
        'name': data.get('name', item['name']),
        'category': data.get('category', item['category']),
        'available': data.get('available', item['available']),
    })
    return jsonify(item), 200

# Delete: Delete an item by ID
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return '', 204

# List All: Get all items
@app.route('/items', methods=['GET'])
def list_all():
    return jsonify(items), 200

# List by Name: Get items by name
@app.route('/items/name/<string:name>', methods=['GET'])
def list_by_name(name):
    filtered_items = [item for item in items if item['name'] == name]
    return jsonify(filtered_items), 200

# List by Category: Get items by category
@app.route('/items/category/<string:category>', methods=['GET'])
def list_by_category(category):
    filtered_items = [item for item in items if item['category'] == category]
    return jsonify(filtered_items), 200

# List by Availability: Get available items
@app.route('/items/available', methods=['GET'])
def list_by_availability():
    available_items = [item for item in items if item['available']]
    return jsonify(available_items), 200

if __name__ == '__main__':
    app.run(debug=True)
