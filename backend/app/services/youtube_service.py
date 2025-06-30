import requests
from datetime import datetime, timedelta
from app.config import (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_TOKEN_URI)

def trocar_codigo_por_token(codigo_autorizacao: str):
    payload = {
        "code": codigo_autorizacao,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(GOOGLE_TOKEN_URI, data=payload)
    return response.json()

def obter_id_do_canal(access_token: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "id,snippet", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        return None, None
    

    canal = dados["items"][0]
    return canal["id"], canal["snippet"]["title"]

def obter_estatisticas_canal(access_token: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "statistics", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        return None
    
    estatisticas = dados["items"][0]["statistics"]

    return {
        "seguidores": int(estatisticas.get("subscriberCount", 0)),
        "total_videos": int(estatisticas.get("videoCount", 0))
    }

def obter_publicacoes_no_periodo(access_token: str, dias: int = 7):
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Authorization": f"Bearer {access_token}"}

    data_final = datetime.utcnow()
    data_inicial = data_final - timedelta(days=dias)

    params = {
        "part": "id",
        "mine": "true",
        "type": "video",
        "maxResults": 50,
        "publishedAfter": data_inicial.isoformat("T") + "Z",
        "publishedBefore": data_final.isoformat("T") + "Z"
    }

    response = requests.get(url, headers=headers, params=params),
    dados = response.json()

    ids_videos = [item["id"]["videoId"] for item in dados.get("items", [])]
    return ids_videos

def filtrar_shorts(access_token: str, videos_ids: list[str]):
    url = "https://www.googleapis.com/youtube/v3/videos"
    headers = {"Authorization": f"Bearer {access_token}"}

    shorts_ids = []

    for i in range(0, len(videos_ids), 50):
        lote = videos_ids[i:i+50]
        params = {
            "part": "contentDetails",
            "id": ",".join(lote)
        }

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    for item in dados.get("items", []):
        duration = item["contentDetails"]["duration"]

        if "M" not in duration and ("S" in duration or duration == "PT0S"):
            shorts_ids.append(item["id"])

    return shorts_ids

def calcular_engajamento_medio(access_token: str, videos_ids: list[str]):
    url = "https://www.googleapis.com/youtube/v3/videos"
    headers = {"Authorization": f"Bearer {access_token}"}

    engajamento_total = 0
    total_videos_validos = 0

    for i in range(0, len(videos_ids), 50):
        lote = videos_ids[i:i+50]
        params = {
            "part": "statistics",
            "id": ",".join(lote)
        }

        response = requests.get(url, headers=headers, params=params)
        dados = response.json()

        for item in dados.get("items", []):
            stats = item["statistics"]
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comentarios = int(stats.get("commentCount", 0))

            if views > 0:
                engajamento = ((likes + comentarios) / views) * 100
                engajamento_total += engajamento
                total_videos_validos += 1
    
    if total_videos_validos == 0:
        return 0
    
    return round(engajamento_total / total_videos_validos, 2)


    

    