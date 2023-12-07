from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class UserRoutes(Blueprint):
    def __init__(self, resource_service, resource_schema):
        super().__init__('user', __name__)
        self.user_service = user_service
        self.user_schema = user_schema
        # For the function where the routes are defined.
        self.userRoutes()

    # Function where the routes are defined.
    def userRoutes(self):
        self.route('/api/sign-up', methods=['POST'])(self.addUser)
        self.route('/api/profile/<int:user_id>', methods=['GET'])(self.getUser)
        self.route('/api/profile/<int:user_id>', methods=['PUT'])(self.updateUser)
        self.route('/api/profile/<int:user_id>', methods=['DELETE'])(self.deleteUser)
    
    def addUser(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.user_id = self.data.get('user_id')
            self.user_name = self.data.get('user_name')
            self.first_name = self.data.get('first_name')
            self.last_name = self.data.get('last_name')
            self.email = self.data.get('email')
            self.avatar = self.data.get('avatar')
            self.password = self.data.get('password')


            try: # Validations for the data
                self.user_id.valiteUser_id(self.user_id)
                self.user_schema.validateUser_name(self.user_name)
                self.user_schema.validateFirst_name(self.first_name)
                self.user_schema.validateLast_name(self.last_name)
                self.user_schema.validateEmail(self.email)
                self.user_schema.validatePassword(self.password)

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data for user', 'details': e.messages}), 400)
            
            # Add a new User with its attributes 
            self.new_user = {
                'user_id':self.user_id,
                'user_name': self.user_name,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'avatar': self.avatar,
                'password': self.password
            }
            self.created_user = self.user_service.addUser(self.new_user)
            return jsonify(self.created_user), 201
        except Exception as e:
            log.critical(f'Error adding a new user to the database: {e}')



    def getUser(self, resource_id):
        self.user = self.user_service.getUser(user_id)
        if self.user:
            return jsonify(self.user), 200
        else: 
            return jsonify({'error': 'User not found'}), 404

       
    def updateUser(self, user_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
             # Updates a User attributes 
            self.user_id = self.data.get('user_id')
            self.user_name = self.data.get('user_name')
            self.first_name = self.data.get('first_name')
            self.last_name = self.data.get('last_name')
            self.email = self.data.get('email')
            self.avatar = self.data.get('avatar')
            self.password = self.data.get('password')


            try: # Validations for the data
                if self.user_id:
                    self.user_schema.validateUserId(self.user_id)
                    
                if self.user_name:
                    self.user_schema.validateUser_name(self.user_name)

                if self.first_name:
                    self.user_schema.validateFirst_name(self.first_name)

                if self.last_name:
                    self.user_schema.validateLast_name(self.last_name)

                if self.email:
                    self.user_schema.validateEmail(self.email)
                
                if self.password:
                    self.user_schema.validatePassword(self.password)

                

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            

            self.user_updated = self.user_service.updateUser(user_id, self.data)

            if self.user_updated:
                return jsonify(self.user_updated), 200
            else:
                return jsonify({'error': 'User not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the user in the database: {e}')


    def deleteUser(self, user_id):
        try:
            self.user_deleted = self.user_service.deleteUser(user_id)
            if self.user_deleted:
                return jsonify(self.user_deleted), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the user in the database: {e}')
