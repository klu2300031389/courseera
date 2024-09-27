from behave import given, when, then
from flask import Flask, jsonify

# Simulated in-memory "database" for products
products_db = []

# Helper function to find a product by ID
def find_product_by_id(product_id):
    return next((product for product in products_db if product['id'] == product_id), None)

# 1. Given the following products exist
@given('the following products exist')
def step_given_products_exist(context):
    """
    Load products into the simulated in-memory database from the feature table.
    """
    for row in context.table:
        product = {
            'id': int(row['id']),
            'name': row['name'],
            'category': row['category'],
            'available': row['available'].lower() == 'true'
        }
        products_db.append(product)

# 2. When I request the list of all products
@when('I request the list of all products')
def step_request_list_all_products(context):
    """
    Return all products in the simulated database.
    """
    context.response = jsonify(products_db)
    context.response_status = 200

# 3. Then I should see {count:d} products
@then('I should see {count:d} products')
def step_see_products_count(context, count):
    """
    Check the number of products in the response.
    """
    response_data = context.response.json
    assert len(response_data) == count, f"Expected {count} products but found {len(response_data)}."

# 4. When I request the product with ID {product_id}
@when('I request the product with ID {product_id:d}')
def step_request_product_by_id(context, product_id):
    """
    Find and return a product by its ID.
    """
    product = find_product_by_id(product_id)
    if product:
        context.response = jsonify(product)
        context.response_status = 200
    else:
        context.response = jsonify({'message': 'Product not found'})
        context.response_status = 404

# 5. Then I should see the product details:
@then('I should see the product details:')
def step_see_product_details(context):
    """
    Validate that the product details match the expected values from the table.
    """
    response_data = context.response.json
    for row in context.table:
        assert str(response_data['id']) == row['id']
        assert response_data['name'] == row['name']
        assert response_data['category'] == row['category']
        assert response_data['available'] == (row['available'].lower() == 'true')

# 6. When I update the product with ID {product_id:d} to have the following details:
@when('I update the product with ID {product_id:d} to have the following details:')
def step_update_product(context, product_id):
    """
    Update the product with the given ID using the data from the table.
    """
    product = find_product_by_id(product_id)
    if not product:
        context.response_status = 404
        context.response = jsonify({'message': 'Product not found'})
        return

    for row in context.table:
        product['name'] = row['name']
        product['category'] = row['category']
        product['available'] = row['available'].lower() == 'true'

    context.response_status = 200
    context.response = jsonify(product)

# 7. Then the product with ID {product_id:d} should have the updated details:
@then('the product with ID {product_id:d} should have the updated details:')
def step_verify_updated_product(context, product_id):
    """
    Verify the updated details of the product.
    """
    product = find_product_by_id(product_id)
    for row in context.table:
        assert product['name'] == row['name']
        assert product['category'] == row['category']
        assert product['available'] == (row['available'].lower() == 'true')

# 8. When I delete the product with ID {product_id:d}
@when('I delete the product with ID {product_id:d}')
def step_delete_product(context, product_id):
    """
    Delete a product by its ID.
    """
    global products_db
    products_db = [product for product in products_db if product['id'] != product_id]
    context.response_status = 200
    context.response = jsonify({'message': 'Product deleted'})

# 9. Then the product with ID {product_id:d} should no longer exist
@then('the product with ID {product_id:d} should no longer exist')
def step_verify_product_deletion(context, product_id):
    """
    Verify that the product with the given ID no longer exists.
    """
    product = find_product_by_id(product_id)
    assert product is None, f"Product with ID {product_id} still exists."

# 10. Then the total number of products should be {count:d}
@then('the total number of products should be {count:d}')
def step_verify_product_count(context, count):
    """
    Check the total number of products in the database.
    """
    assert len(products_db) == count, f"Expected {count} products but found {len(products_db)}."

# 11. When I search for products with the name "{name}"
@when('I search for products with the name "{name}"')
def step_search_by_name(context, name):
    """
    Search for products by their name.
    """
    context.response = jsonify([product for product in products_db if product['name'] == name])
    context.response_status = 200

# 12. When I search for products in category "{category}"
@when('I search for products in category "{category}"')
def step_search_by_category(context, category):
    """
    Search for products by their category.
    """
    context.response = jsonify([product for product in products_db if product['category'] == category])
    context.response_status = 200

# 13. When I search for products that are "{availability}"
@when('I search for products that are "{availability}"')
def step_search_by_availability(context, availability):
    """
    Search for products by availability (true or false).
    """
    is_available = availability.lower() == 'true'
    context.response = jsonify([product for product in products_db if product['available'] == is_available])
    context.response_status = 200
