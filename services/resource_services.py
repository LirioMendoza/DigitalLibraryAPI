from logger.logger_base import log
from flask import jsonify

class ResourceService:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    # Function that obtains the resource with the specified resource_id
    def getResources(self):
        try:
            self.resources = list(self.db_connector.db.resources.find())
            return self.resources
        except Exception as e:
            log.critical(f'Error fetching all resources from the database: {e}')
            return jsonify({'error': f'Error fetching all resources from the database: {e}'}), 500

    # Function that obtains maximum id for the resources and adds a new resource with the subsequent ID.
    def addResource(self, new_resource):
        try:
            self.max_id = self.db_connector.db.resources.find_one(sort=[('_id', -1)])['_id'] if self.db_connector.db.resources.count_documents({}) > 0 else 0
            self.new_id = int(self.max_id) + 1
            new_resource['_id'] = str(self.new_id)
            self.db_connector.db.resources.insert_one(new_resource)
            return new_resource
        except Exception as e:
            log.critical(f'Error creating the new resource: {e}')
            return jsonify({'error': f'Error creating the new resource: {e}'}), 500

    # Function that obtains the resource with the specified resource_id
    def getResourceById(self, resource_id):
        try:
            self.resource = self.db_connector.db.resources.find_one({'_id': str(resource_id)})
            return self.resource
        except Exception as e:
            log.critical(f'Error fetching the resource id from the database: {e}')
            return jsonify({'error': f'Error fetching the resource id from the database: {e}'}), 500

    # Function that obtains the resource with the resource_id and and updates it after comparing if there were changes
    def updateResource(self, resource_id, updated_data):
        try:
            
            updated_resource = self.getResourceById(resource_id)
            if updated_resource:
                result = self.db_connector.db.resources.update_one({'_id': str(resource_id)}, {'$set': updated_data})

                if result.modified_count > 0:
                    return updated_resource
                else:
                    return {'message': 'The resource is already up-to-date'}
            else:
                return None

        except Exception as e:
            log.critical(f'Error updating the resource data: {e}')
            return jsonify({'error': f'Error updating the resource data: {e}'}), 500
        
    # Function that deletes the resource with the specific resource_id         
    def deleteResource(self, resource_id):
        try:
            deleted_resource = self.getResourceById(resource_id)
            if deleted_resource:
                self.db_connector.db.resources.delete_one({'_id': str(resource_id)})
                return deleted_resource
            else:
                return None

        except Exception as e:
            log.critical(f'Error deleting the resource data: {e}')
            return jsonify({'error': f'Error deleting the resource data: {e}'}), 500

    # Function that obtains the PDF file with the specified resource_id
    def getResourcePdf(self, resource_id):
        try:
            self.resource = self.db_connector.db.resources.find_one({'_id': str(resource_id)})
            return self.resource['pdf_url']
        except Exception as e:
            log.critical(f'Error fetching the resource id from the database: {e}')
            return jsonify({'error': f'Error fetching the resource id from the database: {e}'}), 500
