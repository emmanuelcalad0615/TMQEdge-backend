from flask import Blueprint, Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.auth_routes import auth_bp
from routes.api_amplitud import amplitud_bp
from routes.dashboard_controller import dashboard_bp
from utils.db import db
from config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, 
    supports_credentials=True,
    origins=['*']
    ) 

app.config.from_object(Config)  

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(amplitud_bp)
api_bp.register_blueprint(dashboard_bp)

app.register_blueprint(api_bp)


db.init_app(app)

with app.app_context():
    db.create_all()