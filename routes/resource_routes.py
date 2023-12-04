from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class ResourceRoutes(Blueprint):
    def __init__(self, resource_service, resource_schema):
        super().__init__('resource', __name__)
        self.resource_service = resource_service
        self.resource_schema = resource_schema
        self.resourceRoutes()

    def resourceRoutes(self):
        self.route('/api/resources', methods=['GET'])(self.getResources)
        self.route('/api/resources', methods=['POST'])(self.addResource)

    def getResources(self):
        try:
            self.resources = self.resource_service.get_all_resources()
            return jsonify(self.resources), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500

    def addResource(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')
            self.description = self.data.get('description')

            try:
                self.resource_schema.validateTitle(self.title)
                self.resource_schema.validateAuthor(self.author)
                self.resource_schema.validateDescription(self.description)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.new_resource = {
                'title': self.title,
                'author': self.author,
                'description': self.description
            }
            self.created_resource = self.resource_service.addResource(self.new_resource)
            return jsonify(self.created_resource), 201
        except Exception as e:
            log.critical(f'Error adding a new resource to the database: {e}')
