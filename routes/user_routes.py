from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class UserRoutes(Blueprint):
    def __init__(self, user_service, user_schema):
        super().__init__('user', __name__)
        self.user_service = user_service
        self.user_schema = user_schema
        # For the function where the routes are defined.
        self.userRoutes()

    # Function where the routes are defined.
    def userRoutes(self):
        self.route('/api/sign-up', methods=['POST'])(self.addUser)

        self.route('/api/profile/<int:user_id>', methods=['GET'])(self.getUserById)
        self.route('/api/profile/<int:user_id>', methods=['PUT'])(self.updateUser)
        self.route('/api/profile/<int:user_id>', methods=['DELETE'])(self.deleteUser)
    
    # Function that validates user data and calls addUser service for the specified user_id
    def addUser(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.username = self.data.get('username')
            self.first_name = self.data.get('first_name')
            self.last_name = self.data.get('last_name')
            self.email = self.data.get('email')
            self.password = self.data.get('password')

            try: # Validations for the data

                self.user_schema.validateUsername(self.username)
                self.user_schema.validateFirstName(self.first_name)
                self.user_schema.validateLastName(self.last_name)
                self.user_schema.validateEmail(self.email)
                self.user_schema.validatePassword(self.password)

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data for user', 'details': e.messages}), 400)
            
            # Add a new User with its attributes 
            self.new_user = {
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'password': self.password
            }
            self.created_user = self.user_service.addUser(self.new_user)
            return jsonify(self.created_user), 201
        except Exception as e:
            log.critical(f'Error adding a new user to the database: {e}')

 # Function that obtains user data for the specified user_id
    def getUserById(self, user_id):
        self.user = self.user_service.getUserById(user_id)
        if self.user:
            return jsonify(self.user), 200
        else: 
            return jsonify({'error': 'User not found'}), 404

    # Function that validates user data and updates if there are any changes 
    # on them then calls updateUser service for the specified user_id  
    def updateUser(self, user_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
             # User attributes to update
            self.username = self.data.get('username')
            self.first_name = self.data.get('first_name')
            self.last_name = self.data.get('last_name')
            self.email = self.data.get('email')
            self.password = self.data.get('password')

            try: # Validations for the data
                    
                if self.username:
                    self.user_schema.validateUsername(self.username)

                if self.first_name:
                    self.user_schema.validateFirstName(self.first_name)

                if self.last_name:
                    self.user_schema.validateLastName(self.last_name)

                if self.email:
                    self.user_schema.validateEmail(self.email)
                
                if self.password:
                    self.user_schema.validatePassword(self.password)

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            # Updating user
            self.user_updated = self.user_service.updateUser(user_id, self.data)

            if self.user_updated:
                return jsonify(self.user_updated), 200
            else:
                return jsonify({'error': 'User not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the user in the database: {e}')

    #Function to delete user by specified user_id
    def deleteUser(self, user_id):
        try:
            self.user_deleted = self.user_service.deleteUser(user_id)
            if self.user_deleted:
                return jsonify(self.user_deleted), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the user in the database: {e}')
