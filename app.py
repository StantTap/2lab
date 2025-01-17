from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from services import services_list
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# Swagger configurations
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Путь к JSON-файлу Swagger

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Barbershop Services API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

class ServiceList(Resource):
    def get(self):
        """
        Получить список всех услуг.
        """
        return jsonify(services_list)

    def post(self):
        """
        Добавить новую услугу.
        """
        new_service = request.get_json()
        services_list.append(new_service)
        return jsonify(new_service), 201

class Service(Resource):
    def get(self, service_id):
        """
        Получить услугу по ID.
        """
        service = next((s for s in services_list if s['id'] == service_id), None)
        if service:
            return jsonify(service)
        else:
            return {'message': 'Service not found'}, 404

    def put(self, service_id):
        """
        Обновить услугу по ID.
        """
        service = next((s for s in services_list if s['id'] == service_id), None)
        if service:
            data = request.get_json()
            service.update(data)
            return jsonify(service)
        else:
            return {'message': 'Service not found'}, 404

    def delete(self, service_id):
        """
        Удалить услугу по ID.
        """
        global services_list
        services_list = [s for s in services_list if s['id'] != service_id]
        return {'message': 'Service deleted'}

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(ServiceList, '/services')
api.add_resource(Service, '/services/<int:service_id>')

if __name__ == '__main__':
    app.run(debug=True)