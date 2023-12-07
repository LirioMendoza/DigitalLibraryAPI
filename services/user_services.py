from logger.logger_base import log
from flask import jsonify

class UserService:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
    # Function that obtains maximum id for the users and adds a new user with the subsequent ID.
    def addUser(self, new_user):
        try:
           
            max_id = self.db_connector.db.users.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.users.count_documents({}) > 0 else 0
            new_id = int(max_id) + 1
            new_user['_id'] = str(new_id)
            self.db_connector.db.users.insert_one(new_user)
            return new_user
        except Exception as e:
            log.critical(f'Error creating the new user: {e}')
            return jsonify({'error': f'Error creating the new user: {e}'}), 500

    # Function that obtains the user with the specified user_id
    def getUserById(self, user_id):
        try:
            user = self.db_connector.db.users.find_one({'_id': str(user_id)})
            return user
        except Exception as e:
            log.critical(f'Error fetching the user from the database: {e}')
            return jsonify({'error': f'Error fetching the user from the database: {e}'}), 500

    # Function that obtains the user with the user_id and and updates it after comparing if there were changes
    def updateUser(self, user_id, updated_data):
        try:
            updated_user =self.getUserById(user_id)
            if updated_user:
                result = self.db_connector.db.users.update_one({'_id':str(user_id)},{'$set': updated_data})
        
                if result.modified_count>0:
                    return updated_user

                else:
                    return {'message': 'The user is already up-to-date'}
            else:
                return None
                
        except Exception as e:
            log.critical(f'Error updating the user data: {e}')
            return jsonify({'error': f'Error updating the user data: {e}'}), 500

    # Function that deletes the user with the specific user_id  
    def deleteUser(self, user_id):
        try:
            deleted_user = self.getUserById(user_id)
            if deleted_user:
                self.db_connector.db.users.delete_one({'_id': str(user_id)})
                return deleted_user
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the user data: {e}')
            return jsonify({'error': f'Error deleting the user data: {e}'}), 500