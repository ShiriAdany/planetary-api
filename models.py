from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import re

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


class Validation:
    @staticmethod
    def is_valid_email(email):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

    @staticmethod
    def is_valid_name(name):
        return re.match(r'^[A-Za-z]+$', name)

    @staticmethod
    def is_valid_password(password):
        return (
                len(password) >= 8 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[!@#$%^&*]', password)
        )


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class PlanetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Planet
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)
