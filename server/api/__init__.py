# external imports
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from logging.config import dictConfig
from flask_jwt_extended import JWTManager

# internal imports
from api.config import Config
from api.errors import register_error_handlers

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class = Config):
    dictConfig(config_class.LOGGING_INFO)
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(
        app, 
        resources = {
            r'/*': {
                'origins': [app.config.get('CLIENT_URL')]
            }
        },
        supports_credentials = True
    )
    mongo.init_app(app)
    jwt.init_app(app)

    register_error_handlers(app)

    # importing blueprints inside factory function 
    # to avoid circular imports
    from api.auth import auth_bp
    from api.users import user_bp
    from api.networks import net_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(net_bp, url_prefix='/networks')

    return app