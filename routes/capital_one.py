from requests import request as make_request
from flask import Blueprint, request
from ..utils.constants import CAPITALONE_ENDPOINT, CAPITALONE_KEY

REQUEST_HEADERS = {
            "Content-Type": "application/json",
            "Version": "1.0",
            "Authorisation": f"Bearer ${CAPITALONE_KEY}"
        },

capital_one = Blueprint('capital_one', __name__)


@capital_one.route("/wallets/init")
def wallets_new() -> str:
    ''' Initialise a wallet for a new user and return the wallet ID'''
    response = make_request(
        "POST", 
        CAPITALONE_ENDPOINT+"/accounts/create",
        headers = REQUEST_HEADERS,
        data = {
            "accounts": [
                {
                    "balance": 0,
                    "currencyCode": "GBP",
                    "productType": "Debit",
                    "state": "open",
                    "creditLimit": 0
                }
            ]
        }
    )

    return response[0]["accountId"]


@capital_one.route("/wallets/balance/<wallet_id>")
def wallets_balance(wallet_id:str) -> float:
    response = make_request(
        "GET",
        CAPITALONE_ENDPOINT + "/accounts/${wallet_id}",
        headers = REQUEST_HEADERS,
    )

    return response.json()["balance"]