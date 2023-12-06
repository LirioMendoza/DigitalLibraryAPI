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
