# User API endpoints
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define API models for documentation and validation
user_model = api.model('User', {
    'id': fields.String(required=True, description='User ID (UUID)'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'is_admin': fields.Boolean(description='Admin flag'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password (min 6 chars)')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address')
})

@api.route('/')
class UserList(Resource):
    """User list resource - POST creates user, GET retrieves all users"""
    
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """
        Retrieve all users
        
        Returns:
            List of all users (passwords excluded from response)
            
        Status Codes:
            200: Success
        """
        users = facade.get_all_users()
        return users, 200
    
    @api.doc('create_user')
    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Invalid input or email already exists')
    def post(self):
        """
        Create a new user
        
        Request body:
            - first_name (required): User's first name (max 50 chars)
            - last_name (required): User's last name (max 50 chars)
            - email (required): Valid email address (must be unique)
            - password (required): Minimum 6 characters
            
        Returns:
            Created user object (without password)
            
        Status Codes:
            201: User created successfully
            400: Invalid input or email already exists
        """
        data = api.payload
        
        # Call facade to create user
        user, error = facade.create_user(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password']
        )
        
        # Handle errors
        if error:
            api.abort(400, str(error))
        
        return user, 201


@api.route('/<user_id>')
class User(Resource):
    """User resource - GET retrieves user, PUT updates user"""
    
    @api.doc('get_user')
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve user by ID
        
        Args:
            user_id: User ID (UUID)
            
        Returns:
            User object (without password)
            
        Status Codes:
            200: Success
            404: User not found
        """
        user = facade.get_user(user_id)
        
        if not user:
            api.abort(404, f'User {user_id} not found')
        
        return user, 200
    
    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """
        Update user information
        
        Args:
            user_id: User ID (UUID)
            
        Request body (all fields optional):
            - first_name: User's first name
            - last_name: User's last name
            - email: User's email address
            
        Returns:
            Updated user object (without password)
            
        Status Codes:
            200: User updated successfully
            404: User not found
            400: Invalid input
        """
        data = api.payload
        
        # Call facade to update user
        user, error = facade.update_user(user_id, data)
        
        # Handle errors
        if error:
            api.abort(404, error) if error == "User not found" else api.abort(400, str(error))
        
        return user, 200
