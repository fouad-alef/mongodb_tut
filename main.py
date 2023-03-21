# mongodb+srv://fouad89ahmed:<password>@tutorial.bhzeiwx.mongodb.net/?retryWrites=true&w=majority
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient


load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"""mongodb+srv://fouad89ahmed:{password}@tutorial.bhzeiwx.mongodb.net/?retryWrites=true&w=majority"""

client = MongoClient(connection_string)
# print(client)

# view information about database
dbs = client.list_database_names()
print(f"Databases: {dbs}")

# view collections in test
test_db = client.test
collections = test_db.list_collection_names()
print(f'Collections {collections}')


def insert_test_doc():
    collection = test_db.test
    test_doc = {
        "name": "Fouad",
        "type": "test"
    }
    inserted_id = collection.insert_one(test_doc).inserted_id
    print(f"first doc id: {inserted_id}")


# insert_test_doc()
## if database / collection doesn't exist, it creates it
production = client.production
person_collection = production.person_collection


def create_documents():
    """A function the will create many documents
    """
    first_names = ["Fouad", "A", "S", "D"]
    last_names = ["S", "X", "R", "F"]
    ages = [21, 40, 50, 60]
    docs = []
    for f, l, a in zip(first_names, last_names, ages):
        doc = {
            "first_name": f,
            "last_name": l,
            "age": a
        }
        docs.append(doc)

    person_collection.insert_many(docs)


# create_documents()

# Reading Documents
printer = pprint.PrettyPrinter()


def find_all_people():
    people = person_collection.find()

    for person in people:
        printer.pprint(person)


#find_all_people()

def find_fouad():
    fouad = person_collection.find_one({"first_name": "Fouad"})
    printer.pprint(fouad)


find_fouad()

# counting documents


def find_all_people():
    counts = person_collection.count_documents(filter={})
    printer.pprint(f"Num Documents {counts}")


#find_all_people()

# Finding a person by id
# we need to use objectid from bson
def get_person_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id": _id})
    printer.pprint(f"Person by ID: {person}")


get_person_by_id("64196ef57de8229f8eef8cbb")
