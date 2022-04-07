import pytest
from notes.apis import GetByLabel
from main import app
import json
# from flask import session

# get_by_label = GetByLabel()

data1 = {
    "user_name": "akshacccc",
    "name": "Akash",
    "email": "nishant.sh@gmail.com",
    "password": "12345",
    "conf_password": "12345"
}
data = json.dumps(data1)


def test_register():
    response = app.test_client().post('/registration', data=data)
    assert response.status_code == 200


def test_label():
    with app.test_client().session_transaction() as session:
        session['logged_in'] = True

    response = app.test_client().get('/api/getbylabel/hii')
    assert response.status_code == 200
