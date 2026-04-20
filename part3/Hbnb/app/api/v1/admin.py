from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt

from app.services import facade


api = Namespace('admin', description='Administrative operations')


@api.route('/status')
class AdminStatus(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        return {
            'users': len(facade.get_all_users()),
            'places': len(facade.get_all_places()),
            'reviews': len(facade.get_all_reviews()),
            'amenities': len(facade.get_all_amenities()),
        }, 200
