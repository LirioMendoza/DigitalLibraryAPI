from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class CommentRoutes(Blueprint):
    def __init__(self, comment_service, comment_schema):
        super().__init__('comment', __name__)
        self.comment_service = comment_service
        self.comment_schema = comment_schema

        # For the function where the routes are defined.
        self.commentRoutes()

    # Function where the routes are defined.
    def commentRoutes(self):
        self.route('/api/resources/<int:resource_id>/comments', methods=['GET'])(self.getComments)
        self.route('/api/resources/<int:resource_id>/comments', methods=['POST'])(self.addComment)


    def getComments(self, resource_id):
        try:
            self.comments = self.comment_service.getComments()
            return jsonify(self.comments), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500

    def addComment(self, resource_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.comment = self.data.get('comment')
            self.rating = self.data.get('rating')

            try: # Validations for the data
                self.comment_schema.validateTitle(self.title)
                self.comment_schema.validateComment(self.comment)
                self.comment_schema.validateRating(self.rating)

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            # Add a new comment with its attributes 
            self.new_comment = {
                'title': self.title,
                'comment': self.comment,
                'rating': self.rating, 
                'resource_id': resource_id
            }
            self.created_comment = self.comment_service.addComment(self.new_comment)
            return jsonify(self.created_comment), 201
        except Exception as e:
            log.critical(f'Error adding a new comment to the database: {e}')