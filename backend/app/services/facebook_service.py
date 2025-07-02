from app.config import FB_PAGE_ID
import requests
from datetime import datetime, timedelta, UTC

def obter_numero_seguidores(access_token: str):
    url = f"https://graph.facebook.com/v17.0/{FB_PAGE_ID}/insights/page_fans"

    params = {
        "access_token": access_token
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erro ao obter seguidores:", response.status_code, response.text)
        return 0

    data = response.json()
    try:
        return data["data"][0]["values"][-1]["value"]
    except:
        return 0
    
def obter_publicacoes_semana(access_token: str, since: datetime, until: datetime):
    url = f"https://graph.facebook.com/v17.0/{FB_PAGE_ID}/posts"

    params = {
        "access_token": access_token,
        "since": int(since.timestamp()),
        "until": int(until.timestamp()),
        "limit": 100
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erro ao obter publicações:", response.status_code, response.text)
        return []
    
    data = response.json()
    publicacoes = data.get("data", [])
    return publicacoes

def obter_numero_publicacoes_semana(publicacoes):
    return len(publicacoes)

def obter_alcance_total(posts: list, access_token: str):
    total_reach = 0
    for post in posts:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"

        params = {
            "metric": "post_impressions_unique",
            "access_token": access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "post_impressions_unique":
                try:
                    total_reach += item["values"][0]["value"]
                except:
                    pass
    return total_reach

def obter_engajamento_total(posts: list, access_token: str):
    total_engagement = 0
    for post in posts:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"

        params = {
            "metric": "post_engaged_users",
            "access_token": access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "post_engaged_users":
                try:
                    total_engagement += item["values"][0]["value"]
                except:
                    pass

        return total_engagement

def calcular_engajamento_medio(engajamento_total: int, alcance_total: int):
    return (engajamento_total / alcance_total * 100) if alcance_total > 0 else 0

                