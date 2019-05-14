import os

import flask

import zoho


def forword_request(e):
    url = base_url + flask.request.path
    method = flask.request.method
    headers = {k:v for k, v in flask.request.headers.items() if k not in ['Host']}
    data = flask.request.data

    resp = api.make_auth_request(method, url, headers, data)
    return resp.content, resp.status_code, resp.headers.items()


base_url = os.getenv('API_ROOT', 'https://desk.zoho.eu')
if base_url.endswith('/'):
    base_url = base_url[:-1]

api = zoho.API()

app = flask.Flask(__name__)
app.register_error_handler(404, forword_request)
