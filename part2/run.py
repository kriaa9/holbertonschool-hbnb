#!/usr/bin/env python3
"""
Main application entry point for HBnB Evolution API

To run the application:
    python run.py
    
The API will be available at:
    http://localhost:5000/api/v1/users
    
Swagger documentation available at:
    http://localhost:5000/api/docs
"""

import os
from app import create_app

if __name__ == '__main__':
    # Get configuration from environment or use default
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app
    app = create_app(config_name)
    
    # Run the application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
