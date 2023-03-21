import pymongo
from dotenv import find_dotenv, load_dotenv
from beanie.operators import Set

from domain.model import User
import os
import timeit
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie



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


def main_pymongo():
    user1 = {"name": "Alice", "age": 25}
    add_user(user1)

    user2 = {"name": "Bob", "age": 30}
    add_user(user2)

    user1["age"] = 30
    update_user(user1)

    delete_user(user2)

async def initialize():
    client = AsyncIOMotorClient(connection_string)
    await init_beanie(database=client.test_database, document_models=[User])


async def add_user(user: User):
    await user.insert()
    print(f"User {user.name} added to the database.")


async def update_user(user: User):
    await user.update(Set({User.age: user.age}))
    print(f"User {user.name} updated in the database.")


async def delete_user(user: User):
    await user.delete()
    print(f"User {user.name} deleted from the database.")


# async def find_users_by_age(age: int):
#     users = await User.find_all(User.age == age).to_list()
#     print(f"Users found with age {age}: {users}")


async def main():
    await initialize()

    user1 = User(name="Alice", age=25)
    await add_user(user1)

    user2 = User(name="Bob", age=30)
    await add_user(user2)

    user1.age = 30
    await update_user(user1)

    await delete_user(user2)


# Measure the execution time of the pymongo approach
print("Pymongo approach:")
print(timeit.timeit(main_pymongo, number=10))

# Measure the execution time of the beanie approach
print("Beanie approach:")
print(timeit.timeit(lambda: asyncio.run(main()), number=10))

