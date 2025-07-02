from app.config import (IG_USER_ID, APP_SECRET, USER_ACCESS_TOKEN, APP_ID)
from app.database import SessionLocal, obter_token, salvar_token
import requests
from datetime import datetime, timedelta, UTC

def get_token_instagram_valido() -> str | None:
    db = SessionLocal()
    token_salvo = obter_token(db, "facebook")

    if not token_salvo:
        novo_token = obter_token_longo_prazo()
        
        if novo_token:
            salvar_token(db, "facebook", novo_token)

        db.close()
        return novo_token
    
    token_renovado = renovar_token_longo_prazo(token_salvo)
    if token_renovado:
        salvar_token(db, "facebook", token_renovado)
        db.close()
        return token_renovado
    
    db.close()
    return token_salvo

def obter_token_longo_prazo():
    url = "https://graph.facebook.com/v17.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": USER_ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erro ao obter token longo:", response.status_code, response.text)
        return None

    data = response.json()
    return data.get("access_token")

def renovar_token_longo_prazo(token_atual: str) -> str | None:
    url = "https://graph.facebook.com/v17.0/oauth/access_token"

    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": token_atual
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        print(f"Erro ao renovar token: {response.status_code} - {response.text}")
        return None