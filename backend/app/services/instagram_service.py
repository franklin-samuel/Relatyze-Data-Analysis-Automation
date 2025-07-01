from app.config import (IG_USER_ID, APP_SECRET_IG, USER_ACCESS_TOKEN_IG, APP_ID_IG)
import requests
import json

url = "https://graph.facebook.com/v17.0/oauth/access_token"

params = {
    "grant_type": "fb_exchange_token",
    "client_id": APP_ID_IG,
    "client_secret": APP_SECRET_IG,
    "fb_exchange_token": USER_ACCESS_TOKEN_IG,
}

response = requests.get(url, params=params)
data = response.json()
long_access_token = data.get("access_token")


