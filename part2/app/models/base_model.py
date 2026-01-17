# Base model for all entities
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Base model for all entities"""
    
    def __init__(self):
        """Initialize base model with UUID and timestamps"""
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def update(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        """String representation of the model"""
        return f"<{self.__class__.__name__}(id={self.id})>"
