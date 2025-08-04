from flask import Blueprint, jsonify, request
from models import db, Planet, User, planet_schema, planets_schema, Validation
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

main_routes = Blueprint('main_routes', __name__)
auth_routes = Blueprint('auth_routes', __name__)


@main_routes.route('/')
def hello():
    return "Hello, Astronauts!"


@main_routes.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough.")


@main_routes.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough.")


@main_routes.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@main_routes.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    return jsonify(message='That planet does not exist'), 404


@main_routes.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message="There is already a planet by that name"), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name, planet_type=planet_type, home_star=home_star,
                            mass=mass, radius=radius, distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message='You added a planet'), 201


@main_routes.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify(message="You updated a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404


@main_routes.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def remove_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet"), 202
    else:
        return jsonify(message="That planet does not exist"), 404


@main_routes.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    if not Validation.is_valid_email(email):
        return jsonify(message="Invalid mail format")

    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="That email already exists."), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        if Validation.is_valid_name(first_name) and Validation.is_valid_name(last_name) and Validation.is_valid_password(password):
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify(message='User created successfully!'), 201
        else:
            return jsonify(message="Invalid name or weak password"), 400


# -----------------------------Auth Routes--------------------------------------------------


@auth_routes.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@auth_routes.route('/update_user', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = int(request.form['user_id'])
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        if Validation.is_valid_name(first_name) and Validation.is_valid_name(
                last_name) and Validation.is_valid_password(password):
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            db.session.commit()
            return jsonify(message="You updated a user"), 202
        else:
            return jsonify(message="Invalid name or weak password"), 400
    else:
        return jsonify(message="That user does not exist"), 404


@auth_routes.route('/change_password', methods=['PATCH'])
@jwt_required()
def change_password():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify(message="User not found"), 404

    new_password = request.form['password']
    if not new_password:
        return jsonify(message="Password is required"), 400

    if not Validation.is_valid_password(new_password):
        return jsonify(
            message="Password must be at least 8 characters and include uppercase, lowercase, number, and special character"), 400

    user.password = new_password
    db.session.commit()
    return jsonify(message="Password updated successfully"), 200


@auth_routes.route('/remove_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user(user_id: int):
    user = User.query.filter_by(user_id = user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="You deleted a user"), 202
    else:
        return jsonify(message="That user does not exist"), 404

