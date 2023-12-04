from logger.logger_base import log
from flask import jsonify

class ResourceService:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_all_resources(self):
        try:
            self.resources = list(self.db_connector.db.resources.find())
            return self.resources
        except Exception as e:
            log.critical(f'Error fetching all resources from the database: {e}')
            return jsonify({'error': f'Error fetching all resources from the database: {e}'}), 500

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
