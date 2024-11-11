from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config
from app.services.s3 import S3Manager

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize services
    s3_manager = S3Manager(
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
        bucket_name=app.config['S3_BUCKET'],
        endpoint_url=app.config['S3_ENDPOINT']
    )
    
    # Register blueprints
    from app.routes.filesystem_routes import filesystem_bp
    app.register_blueprint(filesystem_bp)
    
    # Add services to app context
    app.s3_manager = s3_manager
    
    return app