from flask_pymongo import PyMongo
from flask import current_app
import bcrypt
from bson.objectid import ObjectId

mongo = PyMongo()


def init_db(app):
    mongo.init_app(app)


def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})


def create_user(name, email, hashed_password):
    mongo.db.users.insert_one(
        {"name": name, "email": email, "password": hashed_password}
    )


def verify_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return user
    return None


# Notes
def create_note(name, description, content, user_id, flowchart_id=None):
    note_data = {
        "name": name.strip(),
        "description": description.strip(),
        "content": content.strip(),
        "user_id": ObjectId(user_id),
        "flowchart_id": flowchart_id.strip() if flowchart_id else None,
    }
    mongo.db.notes.insert_one(note_data)


def get_note(note_id):
    try:
        object_id = ObjectId(note_id)
    except Exception as e:
        print(f"Error converting note_id to ObjectId: {e}")
        return None

    note = mongo.db.notes.find_one({"_id": object_id})
    if not note:
        return None

    user = mongo.db.users.find_one({"_id": note["user_id"]})
    user_info = (
        {"name": user.get("name", ""), "email": user.get("email", "")}
        if user
        else {"name": "", "email": ""}
    )

    return {
        "name": note.get("name", ""),
        "description": note.get("description", ""),
        "content": note.get("content", ""),
        "user_id": str(note.get("user_id", "")),
        "flowchart_id": note.get("flowchart_id", None),
        "user": user_info,
    }


def update_note(note_id, update_fields):
    try:
        object_id = ObjectId(note_id)
    except Exception as e:
        print(f"Error converting note_id to ObjectId: {e}")
        return False

    result = mongo.db.notes.update_one({"_id": object_id}, {"$set": update_fields})
    return result.modified_count > 0


def delete_note(note_id):
    try:
        object_id = ObjectId(note_id)
    except Exception as e:
        print(f"Error converting note_id to ObjectId: {e}")
        return False

    result = mongo.db.notes.delete_one({"_id": object_id})
    return result.deleted_count > 0


def get_all_notes():
    notes = list(mongo.db.notes.find())
    notes_with_user_info = []

    for note in notes:
        user = mongo.db.users.find_one({"_id": note["user_id"]})
        user_info = (
            {"name": user.get("name", ""), "email": user.get("email", "")}
            if user
            else {"name": "", "email": ""}
        )

        notes_with_user_info.append(
            {
                "id": str(note["_id"]),
                "user_id": str(note["user_id"]),
                "name": note.get("name", ""),
                "description": note.get("description", ""),
                "content": note.get("content", ""),
                "flowchart_id": note.get("flowchart_id", None),
                "user": user_info,
            }
        )

    return notes_with_user_info


def get_notes_by_user(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        print(f"Error converting user_id to ObjectId: {e}")
        return []

    notes = list(mongo.db.notes.find({"user_id": object_id}))
    notes_with_user_info = []

    for note in notes:
        user = mongo.db.users.find_one({"_id": note["user_id"]})
        user_info = (
            {"name": user.get("name", ""), "email": user.get("email", "")}
            if user
            else {"name": "", "email": ""}
        )

        notes_with_user_info.append(
            {
                "id": str(note["_id"]),
                "name": note.get("name", ""),
                "description": note.get("description", ""),
                "content": note.get("content", ""),
                "flowchart_id": note.get("flowchart_id", None),
                "user": user_info,
            }
        )

    return notes_with_user_info


# flowcharts
# Create
def create_flowchart(title, file_path, filename):
    result = mongo.db.flowcharts.insert_one(
        {"title": title, "image_path": file_path, "filename": filename}
    )
    return result.inserted_id


# Read
def read_flowchart(flowchart_id):
    result = mongo.db.flowcharts.find_one({"_id": ObjectId(flowchart_id)})
    return result


# Update
def update_flowchart(flowchart_id, update_fields={}):
    result = mongo.db.flowcharts.update_one(
        {"_id": ObjectId(flowchart_id)}, {"$set": update_fields}
    )
    return result.modified_count


# delete
def delete_flowchart(flowchart_id):
    result = mongo.db.flowcharts.delete_one({"_id": ObjectId(flowchart_id)})
    return result.deleted_count
