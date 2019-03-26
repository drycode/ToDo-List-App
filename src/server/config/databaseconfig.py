rconf = {
    'REDIS_HOST' : "localhost",
    'REDIS_PORT' : 6379,
    'REDIS_PASSWORD' : ""
}
google_creds = {
    'CLIENT_ID' : "924099081948-et3iutji8q381r7e72qblsc5fb88cv57.apps.googleusercontent.com",
    'CLIENT_SECRET': "okTLnrmdR26dvslNqO2as8C3",
    'REDIRECT_URI' : "http://localhost:5000/callback/google",
    'AUTHORIZATION_BASE_URL' : "https://accounts.google.com/o/oauth2/v2/auth",
    'TOKEN_URL' : "https://www.googleapis.com/oauth2/v4/token",
    'SCOPE' : ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
}