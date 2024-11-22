from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)

    # importing blueprints inside factory function to avoid circular imports
    from api.auth import auth_bp
    from api.network import net_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(net_bp, url_prefix='/network')

    return app