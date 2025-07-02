from app.config import (IG_USER_ID, APP_SECRET, USER_ACCESS_TOKEN, APP_ID)
from app.services.auth_meta_service import get_token_valido
import requests
from datetime import datetime, timedelta, UTC

def obter_numero_seguidores(ig_user_id: str, access_token: str):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}"
    params = {
        "fields": "followers_count",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erro ao obter seguidores:", response.status_code, response.text)
        return None

    data = response.json()
    return data.get("followers_count")

def obter_publicacoes_semana(ig_user_id: str, access_token: str, since: datetime, until: datetime):
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {
        "fields": "id,caption,timestamp",
        "access_token": access_token,
        "limit": 100,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Erro ao obter publicações:", response.status_code, response.text)
        return []

    data = response.json()
    media = data.get("data", [])
    media_filtrada = []

    for m in media:
        try:
            timestamp = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
            if since <= timestamp <= until:
                media_filtrada.append(m)
        except Exception as e:
            print(f"Erro ao processar timestamp: {e}")

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
        if response.status_code != 200:
            print(f"Erro ao obter alcance de {post['id']}: {response.status_code} {response.text}")
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "reach":
                try:
                    total_reach += item["values"][0]["value"]
                except (IndexError, KeyError) as e:
                    print(f"Erro ao ler valor de alcance: {e}")

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
        if response.status_code != 200:
            print(f"Erro ao obter engajamento de {post['id']}: {response.status_code} {response.text}")
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "engagement":
                try:
                    total_engagement += item["values"][0]["value"]
                except (IndexError, KeyError) as e:
                    print(f"Erro ao ler valor de engajamento: {e}")
    
    return total_engagement

def obter_engajamento_medio(engajamento_total, alcance_total):
    return (engajamento_total / alcance_total * 100) if alcance_total > 0 else 0

# Função principal: apenas orquestra as chamadas
def obter_relatorio_semanal_instagram():
    access_token = get_token_valido()

    if not access_token:
        return {"erro": "Não foi possível obter token válido"}

    ig_user_id = IG_USER_ID
    today = datetime.now(UTC)
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
        "seguidores_fim": seguidores_fim,
        "publicacoes": numero_publicacoes,
        "alcance_total": alcance_total,
        "engajamento_medio": round(engajamento_medio, 2)
    }

print(obter_relatorio_semanal_instagram())