from logger.logger_base import log
from flask import jsonify

class UserService:
    def __init__(self, db_connector):
        self.db_connector = db_connector
    
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

    def getUser(self, user_id):
        try:
            user = self.db_connector.db.users.find_one({'_id': str(user_id)})
            return user
        except Exception as e:
            log.critical(f'Error fetching the user from the database: {e}')
            return jsonify({'error': f'Error fetching the user from the database: {e}'}), 500

    def updateUser(self, user_id, update_data):
        try:
            updated_user =self.getUser(user_id)
            if updated_user:
                result = self.db_connector.db.users.update_one({'_id':str(user_id)},{'$set': updated_user})
                print("Los datos a actualizar son:")
                print(result)
                if result.modified_count>0:
                    return updated_user
                else:
                    return {'message': 'The comment is already up-to-date'}
            else:
                return None
                
        except Exception as e:
            log.critical(f'Error updating the comment data User: {e}')
            return jsonify({'error': f'Error updating the comment data User: {e}'}), 500

    def deleteUser(self, user_id):
        try:
            deleted_user = self.getUser(user_id)
            if deleted_user:
                self.db_connector.db.users.delete_one({'_id': str(user_id)})
                print("Delete User")
                return deleted_user
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the user data: {e}')
            return jsonify({'error': f'Error deleting the user data: {e}'}), 500