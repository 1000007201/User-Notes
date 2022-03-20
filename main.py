import os
from flask import Flask
from flask_restful import Api
from db.utils import connect_db
from routes import all_routes
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))
api = Api(app)
connect_db()


def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == "__main__":
    app.run(debug=True, port=80)

