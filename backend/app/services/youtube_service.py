import requests
from datetime import datetime, timedelta, UTC
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URI,
)
from app.database import (
    salvar_token,
    obter_token,
    salvar_numero_seguidores,
    obter_ultimo_numero_antes,
    SessionLocal,
)


def trocar_codigo_por_token(codigo_autorizacao: str):
    print("[YouTube] Trocando código de autorização por token...")
    payload = {
        "code": codigo_autorizacao,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URI, data=payload)
    dados = response.json()
    print(f"[YouTube] Status response token: {response.status_code}")

    if "access_token" in dados:
        print("[YouTube] Token obtido com sucesso. Salvando no banco de dados.")
        db = SessionLocal()
        salvar_token(db, "youtube", dados["access_token"])
        db.close()
    else:
        print("[YouTube] Falha ao obter token:", dados)

    return dados


def obter_id_e_nome_canal(access_token: str):
    print("[YouTube] Buscando ID e nome do canal...")
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "id,snippet", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    print(f"[YouTube] Status response canal: {response.status_code}")
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        print("[YouTube] Nenhum canal encontrado.")
        return None, None

    canal = dados["items"][0]
    canal_id = canal["id"]
    canal_nome = canal["snippet"]["title"]
    print(f"[YouTube] Canal encontrado: {canal_nome} (ID: {canal_id})")
    return canal_id, canal_nome


def obter_numero_seguidores(access_token: str):
    print("[YouTube] Buscando número de inscritos...")
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"part": "statistics", "mine": "true"}

    response = requests.get(url, headers=headers, params=params)
    print(f"[YouTube] Status response inscritos: {response.status_code}")
    dados = response.json()

    if "items" not in dados or not dados["items"]:
        print("[YouTube] Nenhuma estatística encontrada.")
        return 0

    estatisticas = dados["items"][0]["statistics"]
    inscritos = int(estatisticas.get("subscriberCount", 0))
    print(f"[YouTube] Inscritos atuais: {inscritos}")
    return inscritos


def obter_publicacoes_semana(access_token: str, since: datetime, until: datetime):
    print("[YouTube] Buscando vídeos publicados na semana...")
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
    print(f"[YouTube] Status response vídeos: {response.status_code}")
    dados = response.json()

    video_ids = [item["id"]["videoId"] for item in dados.get("items", [])]
    print(f"[YouTube] {len(video_ids)} vídeos encontrados na semana.")
    return video_ids


def obter_numero_publicacoes_semana(publicacoes: list):
    print(f"[YouTube] Número de publicações na semana: {len(publicacoes)}")
    return len(publicacoes)


def filtrar_shorts(access_token: str, videos_ids: list[str]):
    print("[YouTube] Filtrando shorts entre os vídeos...")
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

    print(f"[YouTube] {len(shorts_ids)} shorts encontrados.")
    return shorts_ids


def obter_engajamento_medio(access_token: str, videos_ids: list[str]):
    print("[YouTube] Calculando engajamento médio dos shorts...")
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

    resultado = round(total_engajamento / total_validos, 2) if total_validos > 0 else 0
    print(f"[YouTube] Engajamento médio: {resultado}%")
    return resultado


def obter_relatorio_semanal_youtube():
    print("Iniciando geração de relatório semanal do YouTube...")
    db = SessionLocal()
    access_token = obter_token(db, "youtube")

    if not access_token:
        print("[YouTube] Token de acesso não encontrado.")
        return {"erro": "Token do YouTube não encontrado"}

    today = datetime.now(UTC)
    start_week = today - timedelta(days=7)

    canal_id, canal_nome = obter_id_e_nome_canal(access_token)
    if not canal_id:
        print("[YouTube] Canal não encontrado.")
        return {"erro": "Não foi possível obter canal do YouTube"}

    seguidores_fim = obter_numero_seguidores(access_token)
    seguidores_inicio = obter_ultimo_numero_antes(db, "youtube", canal_id, start_week)

    if seguidores_fim is not None:
        print(f"[YouTube] Salvando inscritos atuais: {seguidores_fim}")
        salvar_numero_seguidores(db, "youtube", canal_id, canal_nome, seguidores_fim, today)
    else:
        print("[YouTube] seguidores_fim está como None!")

    publicacoes = obter_publicacoes_semana(access_token, start_week, today)
    numero_publicacoes = obter_numero_publicacoes_semana(publicacoes)
    shorts_ids = filtrar_shorts(access_token, publicacoes)
    engajamento_medio = obter_engajamento_medio(access_token, shorts_ids)

    print("✅ Relatório YouTube gerado com sucesso.")
    return {
        "rede_social": "YouTube",
        "canal_id": canal_id,
        "canal_nome": canal_nome,
        "seguidores_inicio": seguidores_inicio,
        "seguidores_fim": seguidores_fim,
        "publicacoes": numero_publicacoes,
        "engajamento_medio": engajamento_medio
    }

print(obter_relatorio_semanal_youtube())
