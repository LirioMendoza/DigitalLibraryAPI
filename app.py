from flask import Flask
from resource.user_models import UserModel
from flask_swagger_ui import get_swaggerui_blueprint
from services.user_services import UserService
from routes.user_routes import UserRoutes
from schemas.user_schemas import UserSchema

from services.user_services import UserService
from routes.user_routes import UserRoutes
from schemas.user_schemas import UserSchema


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

db_connector = UserModel()
db_connector.connectToDatabase()

# For users

user_service = UserService(db_connector)
user_schema = UserSchema()

user_blueprint = UserRoutes(user_service, user_schema)
app.register_blueprint(user_blueprint)


CORS(app, user={r'/api/sign-up': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.closeConnection()

