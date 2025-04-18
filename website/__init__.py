from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from os import path
from .celery import make_celery
from flask_cors import CORS
import redis

db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}}, supports_credentials=True)
    app.config['SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['BASE_URL'] = 'http://localhost:5000'

    app.config['REDIS_URL'] = 'redis://localhost:6379/0'

    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  
    app.config['SESSION_COOKIE_SECURE'] = False  


    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return {}, 200 

    # Mail Configuration
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025  
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None

    # Celery Configuration
    app.config['broker_url'] = 'redis://localhost:6379/0'
    app.config['result_backend'] = 'redis://localhost:6379/0'


    db.init_app(app)
    mail.init_app(app)

    redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'], decode_responses=True)
    app.redis_client = redis_client

    celery = make_celery(app) 
    app.celery = celery  

    from .auth import auth
    from .adm import adm
    from .proff import proff
    from .custo import custo

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(adm, url_prefix='/')
    app.register_blueprint(proff, url_prefix='/')
    app.register_blueprint(custo, url_prefix='/')
    
    from . import models
    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User, Professional

    @login_manager.user_loader
    def load_user(user_email):
        return User.query.get(user_email) or Professional.query.get(user_email)

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')


app = create_app()

celery = app.celery  
from . import tasks
