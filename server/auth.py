import os
import uuid

from flask import jsonify, redirect, request, session, url_for
from flask_httpauth import HTTPBasicAuth, make_response
from requests_oauthlib import OAuth2Session

from server.app import app
from config.databaseconfig import *
from server.redis_local import r


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

# TODO: look into "singleton pattern" for caching modules

client_id = google_creds['CLIENT_ID']
client_secret = google_creds['CLIENT_SECRET']
redirect_uri = google_creds['REDIRECT_URI']
token_url = google_creds['TOKEN_URL']
scope = google_creds['SCOPE']
authorization_base_url = google_creds['AUTHORIZATION_BASE_URL']

def login():
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


def callback():
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['oauth_state'])
    # redirect_response = input(redirect_uri)
    token = google.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_state'] = token
    return jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())

def getsession():
    if 'oauth_state' in session: 
        return jsonify(session['oauth_state'])
    return 'Not logged in'

def logout():
    session['oauth_state'] = None
    return jsonify({"Logout Message": "You have successfully logged out. You will now be redirected."})

# Possibly Junk
# class User():
#     def __init__(self, json_data):
#         self.email = json_data['email']

#     def create_user(self):
#         hash_name = "users"
#         if r.hget(hash_name, self.user_id):
#             return 
#         r.hset(hash_name, self.user_id, str(dict(self.social_id, self.nickname, self.email)))

#     def __str__(self):
#         return self.email
