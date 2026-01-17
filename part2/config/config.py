# Configuration for HBnB Evolution API
import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # API Configuration
    API_TITLE = 'HBnB Evolution API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    
    # RESTX Configuration
    RESTX_MASK_SWAGGER = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
