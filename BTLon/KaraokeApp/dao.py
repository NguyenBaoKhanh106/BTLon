import json
import hashlib

from KaraokeApp import app, login
from KaraokeApp.models import Branch, Room, User


def loadrooms(page=None):
    # with open("data/rooms.json", encoding="utf-8") as f:
    #     return json.load(f)
    query = Room.query
    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        end = start + size
        
        query = query.slice(start, end)
    return query.all()

def loadbranches():
    # with open("data/branches.json", encoding="utf-8") as f:
    #     return json.load(f)
    return Branch.query.all()

def get_room_by_id(room_id):
    # with open("data/rooms.json", encoding="utf-8") as f:
    #     rooms = json.load(f)
    #
    #     for r in rooms:
    #         if str(r["room_id"]) == str(room_id):
    #             return r
    #
    # return None
    return Room.query.get(room_id)

def get_branches_by_id(branch_id):
    # with open("data/branches.json", encoding="utf-8") as f:
    #     branches = json.load(f)
    #     for b in branches:
    #         if str(b["branch_id"]) == str(branch_id):
    #             return b
    #
    # return None
    return Branch.query.get(branch_id)

def count_room():
    return Room.query.count()

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

def auth_user(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


if __name__ == "__main__":
    print(loadrooms())