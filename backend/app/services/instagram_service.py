from app.config import IG_USER_ID
from app.services.auth_meta_service import get_token_valido
import requests
from datetime import datetime, timedelta, UTC
from app.database import SessionLocal, salvar_numero_seguidores, obter_ultimo_numero_antes


def obter_nome_id_perfil(ig_user_id: str, access_token: str) -> tuple[str, str] | tuple[None, None]:
    print("[Instagram] Buscando nome e ID do perfil...")
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}"
    params = {
        "fields": "id,name",
        "access_token": access_token
    }

    response = requests.get(url, params=params)
    print(f"[Instagram] Status response nome perfil: {response.status_code}")
    if response.status_code != 200:
        print("[Instagram] Erro ao obter nome do perfil:", response.status_code, response.text)
        return None, None

    data = response.json()
    perfil_id = data.get("id")
    perfil_nome = data.get("name")
    print(f"[Instagram] Perfil encontrado: {perfil_nome} (ID: {perfil_id})")
    return perfil_id, perfil_nome


def obter_numero_seguidores(ig_user_id: str, access_token: str):
    print("[Instagram] Buscando número de seguidores...")
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}"
    params = {
        "fields": "followers_count",
        "access_token": access_token,
    }

    response = requests.get(url, params=params)
    print(f"[Instagram] Status response seguidores: {response.status_code}")
    if response.status_code != 200:
        print("[Instagram] Erro ao obter seguidores:", response.status_code, response.text)
        return None

    data = response.json()
    seguidores = data.get("followers_count")
    print(f"[Instagram] Seguidores atuais: {seguidores}")
    return seguidores


def obter_publicacoes_semana(ig_user_id: str, access_token: str, since: datetime, until: datetime):
    print("[Instagram] Buscando publicações da semana...")
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {
        "fields": "id,caption,timestamp",
        "access_token": access_token,
        "limit": 100,
    }

    response = requests.get(url, params=params)
    print(f"[Instagram] Status response publicações: {response.status_code}")
    if response.status_code != 200:
        print("[Instagram] Erro ao obter publicações:", response.status_code, response.text)
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
            print(f"[Instagram] Erro ao processar timestamp: {e}")

    print(f"[Instagram] {len(media_filtrada)} publicações dentro do período.")
    return media_filtrada


def obter_alcance(media: list, access_token: str) -> int:
    print("[Instagram] Calculando alcance total...")
    total_reach = 0

    for post in media:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"
        params = {
            "metric": "reach",
            "access_token": access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"[Instagram] Erro ao obter alcance de {post['id']}: {response.status_code} {response.text}")
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "reach":
                try:
                    valor = item["values"][0]["value"]
                    total_reach += valor
                except (IndexError, KeyError) as e:
                    print(f"[Instagram] Erro ao ler valor de alcance: {e}")

    print(f"[Instagram] Alcance total calculado: {total_reach}")
    return total_reach


def obter_engajamento_total(media: list, access_token: str):
    print("[Instagram] Calculando engajamento total...")
    total_engagement = 0

    for post in media:
        url = f"https://graph.facebook.com/v17.0/{post['id']}/insights"
        params = {
            "metric": "engagement",
            "access_token": access_token
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"[Instagram] Erro ao obter engajamento de {post['id']}: {response.status_code} {response.text}")
            continue

        insights = response.json().get("data", [])
        for item in insights:
            if item["name"] == "engagement":
                try:
                    valor = item["values"][0]["value"]
                    total_engagement += valor
                except (IndexError, KeyError) as e:
                    print(f"[Instagram] Erro ao ler valor de engajamento: {e}")
    
    print(f"[Instagram] Engajamento total calculado: {total_engagement}")
    return total_engagement


def obter_engajamento_medio(engajamento_total, alcance_total):
    if alcance_total > 0:
        resultado = (engajamento_total / alcance_total * 100)
        print(f"[Instagram] Engajamento médio: {resultado:.2f}%")
        return resultado
    else:
        print("[Instagram] Alcance total é zero. Engajamento médio será 0.")
        return 0


# Função principal
def obter_relatorio_semanal_instagram():
    print("Iniciando geração de relatório semanal do Instagram...")
    db = SessionLocal()
    access_token = get_token_valido()

    if not access_token:
        print("[Instagram] Token inválido.")
        return {"erro": "Não foi possível obter token válido"}
    
    ig_user_id = IG_USER_ID
    perfil_id, perfil_nome = obter_nome_id_perfil(ig_user_id, access_token)
    today = datetime.now(UTC)
    start_week = today - timedelta(days=7)

    seguidores_inicio = obter_ultimo_numero_antes(db, "instagram", perfil_id, start_week)

    seguidores_fim = obter_numero_seguidores(ig_user_id, access_token)

    if seguidores_fim is not None:
        print(f"[Instagram] Salvando seguidores atuais: {seguidores_fim}")
        salvar_numero_seguidores(db, "instagram", perfil_id, perfil_nome, seguidores_fim, today)
    else:
        print("[Instagram] Seguidores fim está como None!")

    media = obter_publicacoes_semana(ig_user_id, access_token, start_week, today)
    numero_publicacoes = len(media)
    alcance_total = obter_alcance(media, access_token)
    engajamento_total = obter_engajamento_total(media, access_token)
    engajamento_medio = obter_engajamento_medio(engajamento_total, alcance_total)

    print("✅ Relatório Instagram gerado com sucesso.")
    return {
        "rede_social": "Instagram",
        "seguidores_inicio": seguidores_inicio,
        "seguidores_fim": seguidores_fim,
        "publicacoes": numero_publicacoes,
        "alcance_total": alcance_total,
        "engajamento_medio": round(engajamento_medio, 2)
    }

