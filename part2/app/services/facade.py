# Facade for business logic operations
from .persistence import DataRepository
from app.models.user import User

class HBnBFacade:
    """Facade for business logic operations - manages all entity operations"""
    
    def __init__(self):
        """Initialize facade with repository"""
        self.repository = DataRepository()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, first_name: str, last_name: str, email: str, password: str):
        """
        Create a new user
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email
            password: User's password
            
        Returns:
            tuple: (user, error_message) - user is None if error, error_message is None if success
        """
        # Check if email already exists
        if self.repository.get_user_by_email(email):
            return None, "Email already exists"
        
        # Create user instance
        user = User(first_name, last_name, email, password)
        
        # Validate user data
        errors = user.validate()
        if errors:
            return None, errors
        
        # Save to repository
        created_user = self.repository.create_user(user)
        return created_user, None
    
    def get_user(self, user_id: str):
        """
        Get user by ID
        
        Args:
            user_id: The user's ID
            
        Returns:
            User or None: The user if found, None otherwise
        """
        return self.repository.get_user(user_id)
    
    def get_user_by_email(self, email: str):
        """
        Get user by email
        
        Args:
            email: The user's email
            
        Returns:
            User or None: The user if found, None otherwise
        """
        return self.repository.get_user_by_email(email)
    
    def update_user(self, user_id: str, data: dict):
        """
        Update user information
        
        Args:
            user_id: The user's ID
            data: Dictionary of attributes to update
            
        Returns:
            tuple: (user, error_message) - user is None if error
        """
        user = self.repository.get_user(user_id)
        if not user:
            return None, "User not found"
        
        # Update user
        updated_user = self.repository.update_user(user_id, data)
        
        # Validate updated user
        errors = updated_user.validate()
        if errors:
            return None, errors
        
        return updated_user, None
    
    def delete_user(self, user_id: str):
        """
        Delete user by ID (Note: Disabled in Part 2)
        
        Args:
            user_id: The user's ID
            
        Returns:
            tuple: (success, error_message)
        """
        return False, "User deletion is not allowed"
    
    def get_all_users(self):
        """
        Get all users
        
        Returns:
            list: List of all users
        """
        return self.repository.get_all_users()
