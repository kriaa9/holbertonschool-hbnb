# User model
from .base_model import BaseModel
import re
from datetime import datetime

class User(BaseModel):
    """User model with email and password"""
    
    def __init__(self, first_name, last_name, email, password):
        """Initialize User"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # In production, this should be hashed
        self.is_admin = False
    
    def validate(self):
        """Validate user data - returns list of errors or empty list"""
        errors = []
        
        # Validate first_name
        if not self.first_name or len(self.first_name.strip()) == 0:
            errors.append("First name is required")
        elif len(self.first_name) > 50:
            errors.append("First name must be less than 50 characters")
        
        # Validate last_name
        if not self.last_name or len(self.last_name.strip()) == 0:
            errors.append("Last name is required")
        elif len(self.last_name) > 50:
            errors.append("Last name must be less than 50 characters")
        
        # Validate email
        if not self._is_valid_email(self.email):
            errors.append("Invalid email format")
        
        # Validate password
        if not self.password or len(self.password) < 6:
            errors.append("Password must be at least 6 characters")
        
        return errors
    
    @staticmethod
    def _is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def to_dict(self):
        """Convert user to dictionary - NOTE: password is NOT included"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        # Password is intentionally excluded from response
        return data
    
    def __repr__(self):
        """String representation"""
        return f"<User(id={self.id}, email={self.email})>"
