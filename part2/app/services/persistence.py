# In-memory data repository for storing entities
from typing import List, Optional, Dict
from app.models.user import User

class DataRepository:
    """In-memory data repository using singleton pattern"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - ensures only one instance exists"""
        if cls._instance is None:
            cls._instance = super(DataRepository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize repository with empty dictionaries"""
        if self._initialized:
            return
        
        self.users: Dict[str, User] = {}
        self._initialized = True
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, user: User) -> User:
        """
        Create a new user in the repository
        
        Args:
            user: User object to create
            
        Returns:
            User: The created user
        """
        self.users[user.id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: The user's ID
            
        Returns:
            User or None: The user if found, None otherwise
        """
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address
        
        Args:
            email: The user's email
            
        Returns:
            User or None: The user if found, None otherwise
        """
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        """
        Update user attributes
        
        Args:
            user_id: The user's ID
            data: Dictionary of attributes to update
            
        Returns:
            User or None: Updated user if found, None otherwise
        """
        user = self.users.get(user_id)
        if user:
            for key, value in data.items():
                # Don't allow updating certain fields
                if key not in ['id', 'created_at', 'updated_at', 'password']:
                    if hasattr(user, key):
                        setattr(user, key, value)
            user.update()
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user by ID
        
        Args:
            user_id: The user's ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def get_all_users(self) -> List[User]:
        """
        Get all users
        
        Returns:
            List[User]: List of all users
        """
        return list(self.users.values())
