from app.config import IG_USER_ID, APP_SECRET, USER_ACCESS_TOKEN, APP_ID
from app.database import SessionLocal, obter_token, salvar_token
import requests
import socket
from datetime import datetime, timedelta, UTC


def internet_disponivel() -> bool:
    try:
        socket.gethostbyname("google.com")
        return True
    except socket.gaierror:
        return False


def get_token_valido() -> str | None:
    print("[META] Verificando token válido...")

    if not internet_disponivel():
        print("Sem internet. Usando token do config.py")
        return USER_ACCESS_TOKEN

    try:
        db = SessionLocal()
    except Exception as e:
        print("Erro ao conectar ao banco:", e)
        return USER_ACCESS_TOKEN

    try:
        token_salvo = obter_token(db, "meta")

        if not token_salvo:
            print("Nenhum token salvo. Obtendo token longo do config...")
            novo_token = obter_token_longo_prazo()

            if novo_token:
                salvar_token(db, "meta", novo_token)
                return novo_token
            else:
                return USER_ACCESS_TOKEN

        if token_expirou(token_salvo):
            print("Token expirado. Tentando renovar...")
            token_renovado = renovar_token_longo_prazo(token_salvo)
            if token_renovado:
                salvar_token(db, "meta", token_renovado)
                return token_renovado
            else:
                print("Falha na renovação. Usando token do config.py")
                return USER_ACCESS_TOKEN

        print("Token salvo ainda é válido.")
        return token_salvo

    finally:
        db.close()


def obter_token_longo_prazo():
    print("Solicitando token de longo prazo com token do config.py...")
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
    print("Token longo obtido com sucesso.")
    return data.get("access_token")


def renovar_token_longo_prazo(token_atual: str) -> str | None:
    print("Renovando token de longo prazo...")
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
        print("Token renovado com sucesso.")
        return data.get("access_token")
    else:
        print(f"Erro ao renovar token: {response.status_code} - {response.text}")
        return None

def token_expirou(token: str) -> bool:
    url = f"https://graph.facebook.com/debug_token"
    params = {
        "input_token": token,
        "access_token": f"{APP_ID}|{APP_SECRET}"
    }

    response = requests.get(url, params=params)
    print(f"[META] Status verificação token: {response.status_code}")
    if response.status_code != 200:
        print("Erro ao verificar token:", response.text)
        return True  

    data = response.json().get("data", {})
    return not data.get("is_valid", False)

if __name__ == "__main__":
    token = get_token_valido()
    print("Token válido retornado:", token[:60], "...")
