from beanie import init_beanie
from beanie.operators import Set
from domain.model import User
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import find_dotenv, load_dotenv
import asyncio
import os

load_dotenv(find_dotenv("to_ignore/.env"))
password = os.environ.get("MONGODB_PWD")
connection_string = f"""mongodb+srv://fouad89ahmed:{password}@tutorial.bhzeiwx.mongodb.net/?retryWrites=true&w=majority"""


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

    # await find_users_by_age(30)

asyncio.run(main())
