from flask import Flask
from models.resource_models import ResourceModel
from flask_swagger_ui import get_swaggerui_blueprint
from services.resource_services import ResourceService
from routes.resource_routes import ResourceRoutes
from schemas.resource_schemas import ResourceSchema
from flask_cors import CORS

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db_connector = ResourceModel()
db_connector.connect_to_database()

resource_service = ResourceService(db_connector)
resource_schema = ResourceSchema()

resource_blueprint = ResourceRoutes(resource_service, resource_schema)
app.register_blueprint(resource_blueprint)

CORS(app, resources={r'/api/resources': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.close_connection()

