from app.config import (IG_USER_ID, APP_SECRET_IG, USER_ACCESS_TOKEN_IG, APP_ID_IG)
import requests
from datetime import datetime, timedelta

def obter_token_longo_prazo():
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
    return long_access_token

def obter_numero_seguidores(ig_user_id: str, access_token: str):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}"

    params = {
        "fields": "followers_count",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    data = response.json()
    followers_numb = data.get("followers_count")
    return followers_numb

def obter_publicacoes_semana(ig_user_id: str, access_token: str, since: datetime, until: datetime):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"

    params = {
        "fields": "id,caption,timestamp",
        "access_token": access_token,
        "limit": 100,
    }

    response = requests.get(url, params=params)
    media = response.json().get("data", [])

    media_filtrada = []
    for m in media:
        timestamp = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
        if since <= timestamp <= until:
            media_filtrada.append(m)

    return media_filtrada

def obter_numero_publicacoes_semana(publicacoes):
    return len(publicacoes)

def obter_alcance(media: list, access_token: str) -> int:
    total_reach = 0

    for post in media:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"

        params = {
            "metric": "reach",
            "access_token": access_token,
        }

        response = requests.get(url, params=params)
        insights = response.json().get("data", [])

        for item in insights:
            if item["name"] == "reach":
                total_reach += item["values"][0]["value"]

    return total_reach

def obter_engajamento_total(media: list, access_token: str):
    total_engagement = 0

    for post in media:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"

        params = {
            "metric": "engagement",
            "access_token": access_token
        }

        response = requests.get(url, params=params)
        insights = response.json().get("data", [])

        for item in insights:
            if item["name"] == "engagement":
                total_engagement += item["values"][0]["value"]
    
    return total_engagement

def obter_engajamento_medio(engajamento_total, alcance_total):
    return (engajamento_total / alcance_total * 100) if alcance_total > 0 else 0

#Todas as informações reunidas
def obter_relatorio_semanal_instagram():
    access_token = obter_token_longo_prazo()
    ig_user_id = IG_USER_ID

    today = datetime.utcnow()
    start_week = today - timedelta(days=7)

    seguidores_inicio = obter_numero_seguidores(ig_user_id, access_token)
    media = obter_publicacoes_semana(ig_user_id, access_token, start_week, today)
    numero_publicacoes = obter_numero_publicacoes_semana(media)
    seguidores_fim = obter_numero_seguidores(ig_user_id, access_token)
    alcance_total = obter_alcance(media, access_token)
    engajamento_total = obter_engajamento_total(media, access_token)
    engajamento_medio = obter_engajamento_medio(engajamento_total, alcance_total)

    return {
        "rede_social": "Instagram",
        "seguidores_inicio": seguidores_inicio,
        "seguidores_fim":  seguidores_fim,
        "publicacoes": numero_publicacoes,
        "alcance_total": alcance_total,
        "engajamento_medio": round(engajamento_medio, 2)
    }





