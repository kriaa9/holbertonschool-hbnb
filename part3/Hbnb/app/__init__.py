from flask import Flask
from flask_cors import CORS

import config
from app.extensions import db, bcrypt, jwt

from flask_restx import Api
from app.api.v1.admin import api as admin_ns
from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def init_api(app):
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return api


def seed_database():
    from app.models.user import User
    from app.models.amenity import Amenity

    admin_email = 'admin@hbnb.io'
    admin_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
    amenity_seed_data = [
        ('8fb3b623-4f45-4ef6-9623-dca7c8cdb61c', 'WiFi'),
        ('64cacda9-d0de-41e1-9b3b-ca98b27c1e74', 'Swimming Pool'),
        ('b5d29e1c-639b-408e-8ce7-c132dd917760', 'Air Conditioning'),
    ]

    if not User.query.filter_by(email=admin_email).first():
        admin_user = User(
            first_name='Admin',
            last_name='HBnB',
            email=admin_email,
            password='admin1234',
            is_admin=True,
        )
        admin_user.id = admin_id
        db.session.add(admin_user)

    for amenity_id, amenity_name in amenity_seed_data:
        if not Amenity.query.filter_by(name=amenity_name).first():
            amenity = Amenity(name=amenity_name)
            amenity.id = amenity_id
            db.session.add(amenity)

    db.session.commit()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    init_api(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()
        seed_database()
    return app
