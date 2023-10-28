from flask import Blueprint, redirect, session, url_for, current_app
from utils.constants import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN
from authlib.integrations.flask_client import OAuth

auth0 = Blueprint('auth0', __name__)

oauth = OAuth(current_app)

oauth.register(
    "auth0",
    client_id= AUTH0_CLIENT_ID,
    client_secret= AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
    secret_key= "9b9adaa08eeef6feb7b91520585be5a63cb137d9e8c8041c1a8c31c093e5ff09",
)

@auth0.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # The app assumes for a /profile path to be available, change here if it's not
    return redirect("/index")

@auth0.route("/login")
def login():
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth0.callback", _external=True)
    )

@auth0.route("/signup")
def signup():
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth0.callback", _external=True),
        screen_hint="signup"
    )