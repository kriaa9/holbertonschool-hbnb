# Application factory
from flask import Flask
from flask_restx import Api

def create_app(config_name='development'):
    """
    Application factory function
    
    Args:
        config_name: Configuration name (development, testing, production)
        
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    from config.config import config_by_name
    app.config.from_object(config_by_name[config_name])
    
    # Initialize Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB Evolution API',
        description='A complete Booking API for properties and reviews',
        doc='/api/docs'
    )
    
    # Import and register namespaces
    from app.api.v1.resources import users
    
    api.add_namespace(users.api, path='/api/v1/users')
    
    return app
