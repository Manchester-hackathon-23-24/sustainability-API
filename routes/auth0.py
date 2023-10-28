from flask import Blueprint, redirect, session, url_for, current_app
from utils.constants import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN
from authlib.integrations.flask_client import OAuth

auth0 = Blueprint('auth0', __name__)

oauth = OAuth(current_app)

domain = "dev-sfzpomlmit7kg0ct.uk.auth0.com"
client_id = "WMBddWwdbJBkZ3BX6wSBYpxT362qrKnx"
client_secret = "SnhRAcjrZlqO6LyUpyLHBcOwEu6dstNMhvKy9QVrBgvv9P_fQWQR8jaRwbcY60dW"

oauth.register(
    "auth0",
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)

# @auth0.route("/callback", methods=["GET", "POST"])
# def callback():
#     """
#     Callback redirect from Auth0
#     """
#     token = oauth.auth0.authorize_access_token()
#     session["user"] = token
#     # The app assumes for a /profile path to be available, change here if it's not
#     return redirect("/index")

@auth0.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # The app assumes for a /profile path to be available, change here if it's not
    return redirect("/")

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