import pymongo
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv("to_ignore/.env"))
password = os.environ.get("MONGODB_PWD")
connection_string = f"""mongodb+srv://fouad89ahmed:{password}@tutorial.bhzeiwx.mongodb.net/?retryWrites=true&w=majority"""

client = pymongo.MongoClient(connection_string)
db = client.test_database
users_collection = db.users

def add_user(user):
    result = users_collection.insert_one(user)
    print(f"User {user['name']} added to the database with id {result.inserted_id}.")

def update_user(user):
    result = users_collection.update_one({"_id": user["_id"]}, {"$set": {"age": user["age"]}})
    print(f"User {user['name']} updated in the database with {result.modified_count} documents modified.")

def delete_user(user):
    result = users_collection.delete_one({"_id": user["_id"]})
    print(f"User {user['name']} deleted from the database with {result.deleted_count} documents deleted.")

def main():
    user1 = {"name": "Alice", "age": 25}
    add_user(user1)

    user2 = {"name": "Bob", "age": 30}
    add_user(user2)

    user1["age"] = 30
    update_user(user1)

    delete_user(user2)

main()
