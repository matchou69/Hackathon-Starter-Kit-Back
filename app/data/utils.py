from shared import db

def input_to_dictionary(input):
    """
    Convert a GraphQL input object to a dictionary.

    This function recursively extracts values from a GraphQL input object and converts them into a flat dictionary.

    Args:
        input (dict): The input object to convert.

    Returns:
        dict: The flattened dictionary.

    Example Usage:
        input_data = {
            "user": {
                "name": "John",
                "address": {
                    "city": "New York",
                    "zip_code": "10001"
                }
            }
        }
        result = input_to_dictionary(input_data)
    """

    def extract_values(data, parent_key=""):
        dictionary = {}
        for key, value in data.items():
            new_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, dict):
                dictionary.update(extract_values(value, new_key))
            else:
                dictionary[new_key] = value
        return dictionary

    dictionary = {}
    for key, value in input.items():
        if isinstance(value, dict):
            dictionary.update(extract_values(value, key))
        else:
            dictionary[key] = value
    return dictionary

def is_id_usable(id, model):
    """
    Check if an ID is usable in the database.

    This function checks if the provided ID exists in the database table specified by the model.

    Args:
        id: The ID to check.
        model: The SQLAlchemy model representing the database table.

    Returns:
        bool: True if the ID is usable, False otherwise.

    Example Usage:
        user_id = 123
        is_usable = is_id_usable(user_id, UserModel)
    """
    if id is not None:
        temp = db.session.query(model).get(id)
        if temp is not None:
            return True
    return False
