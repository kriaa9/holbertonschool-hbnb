from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
	'text': fields.String(required=True, description='Text of the review'),
	'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
	'user_id': fields.String(required=True, description='ID of the user'),
	'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
	@api.expect(review_model, validate=True)
	@api.response(201, 'Review successfully created')
	@api.response(400, 'Invalid input data')
	@api.response(404, 'User or place not found')
	def post(self):
		"""Register a new review"""
		review_data = api.payload

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

	@api.expect(review_model, validate=False)
	@api.response(200, 'Review updated successfully')
	@api.response(404, 'Review not found')
	@api.response(400, 'Invalid input data')
	def put(self, review_id):
		"""Update a review's information"""
		review_data = api.payload

		try:
			updated_review = facade.update_review(review_id, review_data)
		except ValueError as err:
			message = str(err)
			status_code = 404 if 'not found' in message.lower() else 400
			return {'error': message}, status_code

		if not updated_review:
			return {'error': 'Review not found'}, 404

		return {'message': 'Review updated successfully'}, 200

	@api.response(200, 'Review deleted successfully')
	@api.response(404, 'Review not found')
	def delete(self, review_id):
		"""Delete a review"""
		deleted = facade.delete_review(review_id)
		if not deleted:
			return {'error': 'Review not found'}, 404
		return {'message': 'Review deleted successfully'}, 200
