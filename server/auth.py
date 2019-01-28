from flask import jsonify, redirect, request, session, url_for
from flask_httpauth import HTTPBasicAuth, make_response
import redis
from config.databaseconfig import *
from requests_oauthlib import OAuth2Session
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

r = redis.StrictRedis(host=rconf['REDIS_HOST'], port=rconf['REDIS_PORT'], password=rconf['REDIS_PASSWORD'], decode_responses=True)       

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

def logout():
    pass

class User():
    def __init__(self, json_data):
        self.email = json_data['email']

    def create_user(self):
        hash_name = "users"
        if r.hget(hash_name, self.user_id):
            return 
        r.hset(hash_name, self.user_id, str(dict(self.social_id, self.nickname, self.email)))

    def __str__(self):
        return self.email



# TODO: Create a user database (Redis)
# TODO: Setup Google SSO 
# TODO: User Registration
# auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     r.set("users", username)

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)


