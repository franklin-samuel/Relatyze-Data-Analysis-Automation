import requests
from datetime import datetime, timedelta, UTC
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URI,
)
from app.database import salvar_numero_seguidores, obter_ultimo_numero_antes, SessionLocal

def trocar_codigo_por_token(codigo_autorizacao: str):
    payload = {
        "code": codigo_autorizacao,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URI, data=payload)
    return response.json()

def obter_id_e_nome_canal(access_token: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "id,snippet", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        return None, None

    canal = dados["items"][0]
    return canal["id"], canal["snippet"]["title"]

def obter_numero_seguidores(access_token: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "statistics", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        return 0

    estatisticas = dados["items"][0]["statistics"]
    return int(estatisticas.get("subscriberCount", 0))

def obter_publicacoes_semana(access_token: str, since: datetime, until: datetime):
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Authorization": f"Bearer {access_token}"}

    params = {
        "part": "id",
        "mine": "true",
        "type": "video",
        "maxResults": 50,
        "publishedAfter": since.isoformat("T") + "Z",
        "publishedBefore": until.isoformat("T") + "Z",
    }

    response = requests.get(url, headers=headers, params=params)
    dados = response.json()

    return [item["id"]["videoId"] for item in dados.get("items", [])]

def obter_numero_publicacoes_semana(publicacoes: list):
    return len(publicacoes)

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

def obter_engajamento_medio(access_token: str, videos_ids: list[str]):
    url = "https://www.googleapis.com/youtube/v3/videos"
    headers = {"Authorization": f"Bearer {access_token}"}

    total_engajamento = 0
    total_validos = 0

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
                total_engajamento += engajamento
                total_validos += 1

    return round(total_engajamento / total_validos, 2) if total_validos > 0 else 0

def obter_relatorio_semanal_youtube(access_token: str):
    today = datetime.now(UTC)
    start_week = today - timedelta(days=7)
    db = SessionLocal()
    canal_id, canal_nome = obter_id_e_nome_canal(access_token)

    seguidores_fim = obter_numero_seguidores(access_token)

    seguidores_inicio = obter_ultimo_numero_antes(db, "youtube", canal_id, start_week)

    if seguidores_fim is not None:
        salvar_numero_seguidores(db, "youtube", canal_id, canal_nome, seguidores_fim, today)

    publicacoes = obter_publicacoes_semana(access_token, start_week, today)
    numero_publicacoes = obter_numero_publicacoes_semana(publicacoes)
    shorts_ids = filtrar_shorts(access_token, publicacoes)
    engajamento_medio = obter_engajamento_medio(access_token, shorts_ids)

    return {
        "rede_social": "YouTube",
        "canal_id": canal_id,
        "canal_nome": canal_nome,
        "seguidores_inicio": seguidores_inicio,
        "seguidores_fim": seguidores_fim,
        "publicacoes": numero_publicacoes,
        "engajamento_medio": engajamento_medio
    }
