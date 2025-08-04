from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validate, ValidationError


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


# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         load_instance = True
#         sqla_session = db.session
#
#     @validates("email")
#     def validate_email(self, value):
#         if not Validation.is_valid_email(value):
#             raise ValidationError("Invalid email format.")
#
#     @validates("first_name")
#     def validate_first_name(self, value):
#         if not Validation.is_valid_name(value):
#             raise ValidationError("Invalid first name (letters only).")
#
#     @validates("last_name")
#     def validate_last_name(self, value):
#         if not Validation.is_valid_name(value):
#             raise ValidationError("Invalid last name (letters only).")
#
#     @validates("password")
#     def validate_password(self, value):
#         if not Validation.is_valid_password(value):
#             raise ValidationError(
#                 "Password must be at least 8 characters and include uppercase, lowercase, number, and special character.")
#


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=validate.Regexp(r'^[A-Za-z]+$'))
    last_name = fields.Str(required=True, validate=validate.Regexp(r'^[A-Za-z]+$'))
    password = fields.Str(required=True, validate=[
        validate.Length(min=8),
        validate.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$', error="Invalid password"),
    ])

class PlanetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Planet
        load_instance = True
        sqla_session = db.session


user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)
