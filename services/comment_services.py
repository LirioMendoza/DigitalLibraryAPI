from logger.logger_base import log
from flask import jsonify

class CommentService:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    # Function that obtains the comment with the specified resource_id
    def getComments(self):
        try:
            self.comments = list(self.db_connector.db.comments.find())
            return self.comments
        except Exception as e:
            log.critical(f'Error fetching all comments from the database: {e}')
            return jsonify({'error': f'Error fetching all comments from the database: {e}'}), 500

    # Function that obtains maximum id for the resources and adds a new comment with the subsequent ID.
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
    
    # Function that obtains the comment with the specified comment_id
    def getCommentById(self, comment_id):
        try:
            self.comment = self.db_connector.db.comments.find_one({'_id': str(comment_id)})
            return self.comment
        except Exception as e:
            log.critical(f'Error fetching the comment id from the database: {e}')
            return jsonify({'error': f'Error fetching the commit id from the database: {e}'}), 500

    # Function that obtains the comment with the comment_id and and updates it after comparing if there were changes
    def updateComment(self, comment_id, updated_data):
        try:
            updated_comment = self.getCommentById(comment_id)
            if updated_comment:
                result = self.db_connector.db.comments.update_one({'_id': str(comment_id)}, {'$set': updated_data})

                if result.modified_count > 0:
                    return updated_comment
                else:
                    return {'message': 'The comment is already up-to-date'}
            else:
                return None

        except Exception as e:
            log.critical(f'Error updating the comment data: {e}')
            return jsonify({'error': f'Error updating the comment data: {e}'}), 500
        
    # Function that deletes the comment with the specific comment_id     
    def deleteComment(self, comment_id):
        try:
            deleted_comment = self.getCommentById(comment_id)
            if deleted_comment:
                self.db_connector.db.comments.delete_one({'_id': str(comment_id)})
                return deleted_comment
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the comment data: {e}')
            return jsonify({'error': f'Error deleting the comment data: {e}'}), 500
