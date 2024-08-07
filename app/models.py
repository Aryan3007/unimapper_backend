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


# projects
def create_project(title="", content="", description="", user_id=None):

    if not user_id:
        raise ValueError("User ID must be provided")

    mongo.db.projects.insert_one(
        {
            "title": title,
            "content": content,
            "description": description,
            "user_id": user_id,
        }
    )


def delete_project(project_id):
    result = mongo.db.projects.delete_one({"_id": ObjectId(project_id)})
    return result.deleted_count > 0


def update_project(project_id, update_fields):
    result = mongo.db.projects.update_one(
        {"_id": ObjectId(project_id)}, {"$set": update_fields}
    )
    return result.modified_count > 0


def get_project(project_id):
    try:
        object_id = ObjectId(project_id)
    except Exception as e:
        print(f"Error converting project_id to ObjectId: {e}")
        return None

    project = mongo.db.projects.find_one({"_id": object_id})

    if not project:
        return None

    user_id = project.get("user_id")
    user = None

    if user_id:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    return {
        "title": project.get("title", ""),
        "content": project.get("content", ""),
        "description": project.get("description", ""),
        "user": {
            "email": user.get("email", "") if user else "",
            "name": user.get("name", "") if user else "",
        },
    }


def get_projects_by_user(user_id):

    projects = mongo.db.projects.find({"user_id": user_id})

    project_list = []
    for project in projects:
        project_list.append(
            {
                "id": str(project["_id"]),
                "title": project["title"],
                "content": project["content"],
                "description": project["description"],
            }
        )

    return project_list
