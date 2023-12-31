from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class ResourceRoutes(Blueprint):
    def __init__(self, resource_service, resource_schema):
        super().__init__('resource', __name__)
        self.resource_service = resource_service
        self.resource_schema = resource_schema
        # For the function where the routes are defined.
        self.resourceRoutes()

    # Function where the routes are defined.
    def resourceRoutes(self):
        self.route('/api/resources', methods=['GET'])(self.getResources)
        self.route('/api/resources', methods=['POST'])(self.addResource)

        self.route('/api/resources/<int:resource_id>', methods=['GET'])(self.getResourceById)
        self.route('/api/resources/<int:resource_id>', methods=['PUT'])(self.updateResource)
        self.route('/api/resources/<int:resource_id>', methods=['DELETE'])(self.deleteResource)
        
        self.route('/api/resources/<int:resource_id>/pdf', methods=['GET'])(self.getResourcePdf)

    # Function to obtain resources data by specified resource_id
    def getResources(self):
        try:
            self.resources = self.resource_service.getResources()
            return jsonify(self.resources), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500

    # Function that validates resource data and calls addResource service for the specified resource_id
    def addResource(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')
            self.description = self.data.get('description')
            self.pdf_url = self.data.get('pdf_url')
            self.book_cover = self.data.get('book_cover')

            try: # Validations for the data
                self.resource_schema.validateTitle(self.title)
                self.resource_schema.validateAuthor(self.author)
                self.resource_schema.validateDescription(self.description)
                self.resource_schema.validateURL(self.pdf_url)
                self.resource_schema.validateURL(self.book_cover)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            # Add a new Resource with its attributes 
            self.new_resource = {
                'title': self.title,
                'author': self.author,
                'description': self.description,
                'pdf_url': self.pdf_url,
                'book_cover': self.book_cover
            }
            self.created_resource = self.resource_service.addResource(self.new_resource)
            return jsonify(self.created_resource), 201
        except Exception as e:
            log.critical(f'Error adding a new resource to the database: {e}')

    # Function that obtains resource data for the specified resource_id
    def getResourceById(self, resource_id):
        self.resource = self.resource_service.getResourceById(resource_id)
        if self.resource:
            return jsonify(self.resource), 200
        else: 
            return jsonify({'error': 'Resource not found'}), 404

    # Function that validates resource data and updates if there are any changes on them
    # then calls updateResource service for the specified resource_id       
    def updateResource(self, resource_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
             # Resource attributes to update

            self.title = self.data.get('title')
            self.author = self.data.get('author')
            self.description = self.data.get('description')
  
            self.pdf_url = self.data.get('pdf_url')
            self.book_cover =self.data.get('book_cover')

            try: # Validations for the data
                if self.title:
                    self.resource_schema.validateTitle(self.title)

                if self.author:
                    self.resource_schema.validateAuthor(self.author)

                if self.description:
                    self.resource_schema.validateDescription(self.description)

                if self.pdf_url:
                    self.resource_schema.validateURL(self.pdf_url)

                if self.book_cover:
                    self.resource_schema.validateURL(self.book_cover)

            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            

            self.resource_updated = self.resource_service.updateResource(resource_id, self.data)

            # Updating comment
            if self.resource_updated:
                return jsonify(self.resource_updated), 200
            else:
                return jsonify({'error': 'Resource not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the resource in the database: {e}')

    #Function to delete resource by specified resource_id
    def deleteResource(self, resource_id):
        try:
            self.resource_deleted = self.resource_service.deleteResource(resource_id)
            if self.resource_deleted:
                return jsonify(self.resource_deleted), 200
            else:
                return jsonify({'error': 'Resource not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the resource in the database: {e}')

    # Function that obtains PDF file data for the specified resource_id
    def getResourcePdf(self, resource_id):
        self.resource_pdf = self.resource_service.getResourcePdf(resource_id)
        if self.resource_pdf:
            return jsonify(self.resource_pdf), 200
        else: 
            return jsonify({'error': 'PDF file not found'}), 404

        
