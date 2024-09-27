from behave import given, when, then
from myapp.models import Item  # Assuming you're loading data into an 'Item' model or similar

# Sample in-memory database for demonstration purposes (in real use case, connect to an actual DB)
database = []

# Step to load BDD data
@given('the following items exist')
def step_load_items(context):
    """
    Load items into the mock database.
    The table is passed from the feature file.
    """
    # Iterate over the table rows provided in the feature file
    for row in context.table:
        # Assuming the table has columns: name, category, and available
        item = {
            'name': row['name'],
            'category': row['category'],
            'available': row['available'].lower() == 'true'
        }
        # In a real scenario, you would insert into a database
        # For example: Item.objects.create(**item)
        database.append(item)

# Step to validate that items were loaded correctly
@then('the database should have {count:d} items')
def step_validate_item_count(context, count):
    """
    Validate the number of items loaded into the mock database.
    """
    assert len(database) == count, f"Expected {count} items, but found {len(database)}."

# Step to check if an item with a specific name exists
@then('an item named "{item_name}" should exist')
def step_check_item_existence(context, item_name):
    """
    Check that an item with the given name exists in the mock database.
    """
    item_exists = any(item['name'] == item_name for item in database)
    assert item_exists, f"Item with name {item_name} not found."

# Additional steps can be defined here as needed for your BDD scenarios
