from flask import Blueprint, request, redirect, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from oauthlib.oauth2 import WebApplicationClient
import json
import requests
from config import Auth
from models import User

bp = Blueprint('google_auth',__name__ )

client = WebApplicationClient(Auth.CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(Auth.DISCOVERY_URL).json()


@bp.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(authorization_endpoint,
                                             redirect_uri=Auth.REDIRECT_URI,
                                             scope=Auth.SCOPE)
    return redirect(request_uri)


@bp.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(token_endpoint,
                                                            authorization_response=request.url,
                                                            redirect_url=request.base_url,
                                                            code=code)
    token_response = requests.post(token_url,
                                   headers=headers,
                                   data=body,
                                   auth=(Auth.CLIENT_ID, Auth.CLIENT_SECRET))
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri,
                                     headers=headers,
                                     data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        avatar = userinfo_response.json()["picture"]
        name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    if not User.get(unique_id):
        User.create(unique_id, name, email, avatar)
    user = User.get(unique_id)
    print(user.id,user.name, user.email, user.avatar)

    login_user(user)
    return redirect(url_for('index'))


@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))









