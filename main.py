import os
from flask import Flask
from flask_restful import Api
from db.utils import connect_db
from routes import all_routes
from flask_caching import Cache
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))
api = Api(app)

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

connect_db()


def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == "__main__":
    app.run(debug=True, port=80)

