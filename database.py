import os
import tempfile
from tinydb import TinyDB, Query

# Initialize the database
temp_dir = tempfile.gettempdir()
db_file = os.path.join(temp_dir, 'new_database.json')

# If the file doesn't exist, create it and add some initial users
if not os.path.exists(db_file):
    db = TinyDB(db_file)

    users_table = db.table('users')
    users_table.insert({'username': 'user1', 'user_id': '0001'})
    users_table.insert({'username': 'user2', 'user_id': '0002'})
    print("Database created and initial users added.")

    api_keys_table = db.table('api_keys')
    api_keys_table.insert({'api_key': '1234'})
    api_keys_table.insert({'api_key': '5678'})
else:
    # If the file exists, just load it
    db = TinyDB(db_file)
    users_table = db.table('users')
   
    api_keys_table = db.table('api_keys')
    
    print("Database loaded.")

# Utility functions
def get_all_users():
    """Fetch all users."""
    return users_table.all()

def find_user_by_id(user_id):
    """Find a user by user_id."""
    User = Query()
    return users_table.search(User.user_id == user_id)

def find_user_by_username(username):
    """Find a user by username."""
    User = Query()
    return users_table.search(User.username == username)

def add_user(user_id, username):
    """Add a new user."""
    users_table.insert({"user_id": user_id, "username": username})

def update_user(user_id, username):
    """Update a user."""
    User = Query()
    return users_table.update({"username": username}, User.user_id == user_id)

def delete_user(user_id):
    """Delete a user."""
    User = Query()
    return users_table.remove(User.user_id == user_id)

def verify_api_key(request_api_key):
    """Verify API key."""
    API_KEY_QUERY = Query()
    api_key = api_keys_table.search(API_KEY_QUERY.api_key == request_api_key)

    return True