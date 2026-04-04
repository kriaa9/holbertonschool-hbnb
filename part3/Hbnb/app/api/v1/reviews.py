from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
	'text': fields.String(required=True, description='Text of the review'),
	'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
	'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
	'text': fields.String(description='Text of the review'),
	'rating': fields.Integer(description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
	@jwt_required()
	@api.expect(review_create_model, validate=True)
	@api.response(201, 'Review successfully created')
	@api.response(400, 'Invalid input data')
	@api.response(404, 'Place not found')
	def post(self):
		"""Register a new review"""
		current_user = get_jwt_identity()
		review_data = dict(api.payload)

		place = facade.get_place(review_data['place_id'])
		if not place:
			return {'error': 'Place not found'}, 404

		if place.owner.id == current_user:
			return {'error': 'You cannot review your own place.'}, 400

		already_reviewed = any(review.user.id == current_user for review in place.reviews)
		if already_reviewed:
			return {'error': 'You have already reviewed this place.'}, 400

		review_data['user_id'] = current_user

		try:
			review = facade.create_review(review_data)
		except ValueError as err:
			message = str(err)
			status_code = 404 if 'not found' in message.lower() else 400
			return {'error': message}, status_code

		return {
			'id': review.id,
			'text': review.text,
			'rating': review.rating,
			'user_id': review.user.id,
			'place_id': review.place.id,
		}, 201

	@api.response(200, 'List of reviews retrieved successfully')
	def get(self):
		"""Retrieve a list of all reviews"""
		reviews = facade.get_all_reviews()
		return [
			{
				'id': review.id,
				'text': review.text,
				'rating': review.rating,
				'user_id': review.user.id,
				'place_id': review.place.id,
			}
			for review in reviews
		], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
	@api.response(200, 'Review details retrieved successfully')
	@api.response(404, 'Review not found')
	def get(self, review_id):
		"""Get review details by ID"""
		review = facade.get_review(review_id)
		if not review:
			return {'error': 'Review not found'}, 404

		return {
			'id': review.id,
			'text': review.text,
			'rating': review.rating,
			'user_id': review.user.id,
			'place_id': review.place.id,
		}, 200

	@jwt_required()
	@api.expect(review_update_model, validate=True)
	@api.response(200, 'Review updated successfully')
	@api.response(404, 'Review not found')
	@api.response(403, 'Unauthorized action')
	@api.response(400, 'Invalid input data')
	def put(self, review_id):
		"""Update a review's information"""
		current_user = get_jwt_identity()
		review = facade.get_review(review_id)
		if not review:
			return {'error': 'Review not found'}, 404
		if review.user.id != current_user:
			return {'error': 'Unauthorized action'}, 403

		review_data = dict(api.payload)

		try:
			updated_review = facade.update_review(review_id, review_data)
		except ValueError as err:
			message = str(err)
			status_code = 404 if 'not found' in message.lower() else 400
			return {'error': message}, status_code

		if not updated_review:
			return {'error': 'Review not found'}, 404

		return {'message': 'Review updated successfully'}, 200

	@jwt_required()
	@api.response(200, 'Review deleted successfully')
	@api.response(404, 'Review not found')
	@api.response(403, 'Unauthorized action')
	def delete(self, review_id):
		"""Delete a review"""
		current_user = get_jwt_identity()
		review = facade.get_review(review_id)
		if not review:
			return {'error': 'Review not found'}, 404
		if review.user.id != current_user:
			return {'error': 'Unauthorized action'}, 403

		deleted = facade.delete_review(review_id)
		if not deleted:
			return {'error': 'Review not found'}, 404
		return {'message': 'Review deleted successfully'}, 200
