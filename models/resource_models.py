import os
from pymongo import MongoClient
from logger.logger_base import log
from dotenv import load_dotenv

class ResourceModel:
    def __init__(self):
        self.client = None
        self.db = None

    def connectToDatabase(self):
        load_dotenv()
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        required_variables = {'MONGODB_USER': mongodb_user, 'MONGODB_PASS': mongodb_pass, 'MONGODB_HOST': mongodb_host}

        for var, val in required_variables.items():
            if not val:
                log.critical(f'{var} variable not found')
                raise ValueError(f'Set {var} variable')

        try:
            self.client = MongoClient(
                host=mongodb_host,
                port=27017,
                username=mongodb_user,
                password=mongodb_pass,
                authSource='admin',
                authMechanism='SCRAM-SHA-256'
            )
            self.db = self.client['library-bd']
        except Exception as e:
            log.critical(f'Failed to connect to the database: {e}')
            raise

    def closeConnection(self):
        if self.client:
            self.client.close()
