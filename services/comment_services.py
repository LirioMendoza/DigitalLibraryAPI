from logger.logger_base import log
from flask import jsonify

class CommentService:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def getComments(self):
        try:
            self.comments = list(self.db_connector.db.comments.find())
            return self.comments
        except Exception as e:
            log.critical(f'Error fetching all comments from the database: {e}')
            return jsonify({'error': f'Error fetching all comments from the database: {e}'}), 500

    def addComment(self, new_comment):
        try:
            self.max_id = self.db_connector.db.comments.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.comments.count_documents({}) > 0 else 0
            self.new_id = int(self.max_id) + 1
            new_comment['_id'] = str(self.new_id)
            self.db_connector.db.comments.insert_one(new_comment)
            return new_comment
        except Exception as e:
            log.critical(f'Error creating the new comments: {e}')
            return jsonify({'error': f'Error creating the new comments: {e}'}), 500
