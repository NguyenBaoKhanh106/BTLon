import json

from flask_login import UserMixin

from KaraokeApp import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from datetime import datetime
from enum import Enum as RoleEnum
from sqlalchemy.orm import relationship

class UserRoleEnum(RoleEnum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    username = Column(String(100),unique=True, nullable=False)
    password = Column(String(100),nullable=False)
    phone = Column(String(15),nullable=False)
    email = Column(String(250))
    avatar = Column(String(500), default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_nLCu85ayoTKwYw6alnvrockq5QBT2ZWR2g&s')
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now)

    def get_id(self):
        return str(self.user_id)

    def __str__(self):
        return self.name

class Branch(db.Model):
    __tablename__ = "branches"
    branch_id = Column(String(20), primary_key=True)
    name = Column(String(150), nullable=False)
    address = Column(String(300), nullable=False)
    city = Column(String(150), nullable=False)
    rooms = relationship("Room", backref="branch", lazy=True)

    def __str__(self):
        return self.name

class Room(db.Model):
    __tablename__ = "rooms"
    room_id = Column(String(20), primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    capacity = Column(Integer, default=15)
    hourly_rate = Column(Float, default=0.0)
    image = Column(String(500))
    status = Column(String(150), default="Available")
    description = Column(String(500))

    branch_id = Column(String(20), ForeignKey('branches.branch_id'), nullable=False)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        with open("data/branches.json", encoding="utf-8") as f:
            branches_data = json.load(f)
            for b in branches_data:
                db.session.add(Branch(**b))
        db.session.commit()

        with open("data/rooms.json", encoding="utf-8") as f:
            rooms_data = json.load(f)
            for r in rooms_data:
                db.session.add(Room(**r))
        db.session.commit()