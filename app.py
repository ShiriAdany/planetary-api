from flask import Flask
from flask_jwt_extended import JWTManager
import os
from models import db, ma
from commands import register_commands
from routes import main_routes,auth_routes

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
register_commands(app)

app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)


if __name__ == '__main__':
    app.run(debug=True)
