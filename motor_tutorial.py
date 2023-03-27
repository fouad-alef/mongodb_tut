from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import find_dotenv, load_dotenv
import asyncio
import os
from domain.model import User

load_dotenv(find_dotenv("to_ignore/.env"))
password = os.environ.get("MONGODB_PWD")
connection_string = f"""mongodb+srv://fouad89ahmed:{password}@tutorial.bhzeiwx.mongodb.net/?retryWrites=true&w=majority"""

# connecting client
# client = AsyncIOMotorClient(connection_string)

# # create db
# db = client.test_database
# # collection
# collection = db.test_collection


async def initialize():
    client = AsyncIOMotorClient(connection_string)
    test_database = client.test_database
    print(f"{test_database}")
    # test_collection = test_database.test_collection
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



loop = client.get_io_loop()
loop.run_until_complete(do_insert())