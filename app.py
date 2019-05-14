import os

import datetime
import flask
import requests


class API(object):
    def __init__(self):
        self._token = None
        self._url = os.getenv('ACCESS_TOKEN_URL', 'https://accounts.zoho.eu/oauth/v2/token')
        self._scope = os.getenv('TOKEN_SCOPE', 'Desk.tickets.READ')
        self._client_id = os.getenv('CLIENT_ID')
        self._client_secret = os.getenv('CLIENT_SECRET')
        self._redirect_uri = os.getenv('REDIRECT_URI')
        self._refresh_token = os.getenv('REFRESH_TOKEN')
        self._org_id = os.getenv('ORG_ID')

    def _is_configured(self):
        if all([self._client_id, self._client_secret, self._redirect_uri,
                self._refresh_token, self._org_id]):
            return True
        return False

    def _has_expired(self):
        if self._expires:
            return datetime.datetime.utcnow() > self._expires

    def _refresh(self):
        payload = {
                "grant_type": "refresh_token",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "redirect_uri": self._redirect_uri,
                "refresh_token": self._refresh_token,
                "scope": self._scope
        }
        now = datetime.datetime.utcnow()
        r = requests.post(self._url, data=payload)
        r.raise_for_status()
        self._raw = r.json()
        self._token = self._raw.get('access_token')
        expires_in = self._raw.get('expires_in')
        self._expires = now + datetime.timedelta(milliseconds=expires_in)

    def make_auth_request(self, url, headers={}, data=None, **kwargs):
        if not self._is_configured():
            return ({
                "message": "settings missing, make sure you have all "
                           "the required settings as environment variables"
            }), 503
        if not self._token or self._has_expired():
            self._refresh()

        headers.update({
            "orgId": self._org_id,
            "Authorization": ' '.join(["Zoho-oauthtoken", self._token])
        })

        r = requests.request(flask.request.method, url,
                             headers=headers, data=data, **kwargs)

        return r.json(), r.status_code


def forword_request(e):
    request_path = flask.request.path
    url = base_url + request_path

    data, code = api.make_auth_request(url, data=flask.request.data)
    return flask.jsonify(data), code


base_url = os.getenv('API_ROOT', 'https://desk.zoho.eu')
if base_url.endswith('/'):
    base_url = base_url[:-1]

api = API()

app = flask.Flask(__name__)
app.register_error_handler(404, forword_request)
