#!/usr/bin/env python3
"""
Unit tests for User API endpoints
"""

import unittest
import json
from app import create_app

class UserAPITestCase(unittest.TestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def tearDown(self):
        """Clean up after each test"""
        self.ctx.pop()
    
    # ==================== CREATE USER TESTS ====================
    
    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/', 
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertFalse(data['is_admin'])
        self.assertNotIn('password', data)  # Password should not be in response
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_create_user_missing_first_name(self):
        """Test user creation fails with missing first name"""
        response = self.client.post('/api/v1/users/',
            json={
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_email(self):
        """Test user creation fails with invalid email"""
        response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'invalid-email',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_short_password(self):
        """Test user creation fails with short password"""
        response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': '123'  # Less than 6 characters
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_duplicate_email(self):
        """Test user creation fails with duplicate email"""
        # Create first user
        self.client.post('/api/v1/users/',
            json={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'duplicate@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'duplicate@example.com',
                'password': 'password456'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    # ==================== GET USER TESTS ====================
    
    def test_get_user_success(self):
        """Test successful user retrieval by ID"""
        # Create a user first
        create_response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        user_id = json.loads(create_response.data)['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], 'Alice')
        self.assertEqual(data['email'], 'alice@example.com')
        self.assertNotIn('password', data)
    
    def test_get_user_not_found(self):
        """Test user retrieval fails for non-existent user"""
        response = self.client.get('/api/v1/users/non-existent-id')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create multiple users
        for i in range(3):
            self.client.post('/api/v1/users/',
                json={
                    'first_name': f'User{i}',
                    'last_name': f'Test{i}',
                    'email': f'user{i}@example.com',
                    'password': 'password123'
                },
                content_type='application/json'
            )
        
        # Get all users
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        
        # Verify password is not in responses
        for user in data:
            self.assertNotIn('password', user)
    
    # ==================== UPDATE USER TESTS ====================
    
    def test_update_user_success(self):
        """Test successful user update"""
        # Create a user first
        create_response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'email': 'bob@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        user_id = json.loads(create_response.data)['id']
        
        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}',
            json={
                'first_name': 'Robert',
                'last_name': 'Wilson-Smith'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Robert')
        self.assertEqual(data['last_name'], 'Wilson-Smith')
        self.assertEqual(data['id'], user_id)
    
    def test_update_user_not_found(self):
        """Test user update fails for non-existent user"""
        response = self.client.put('/api/v1/users/non-existent-id',
            json={'first_name': 'Updated'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_update_user_invalid_email(self):
        """Test user update fails with invalid email"""
        # Create a user first
        create_response = self.client.post('/api/v1/users/',
            json={
                'first_name': 'Carol',
                'last_name': 'Brown',
                'email': 'carol@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        
        user_id = json.loads(create_response.data)['id']
        
        # Try to update with invalid email
        response = self.client.put(f'/api/v1/users/{user_id}',
            json={'email': 'invalid-email'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
