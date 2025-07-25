from app.config import FB_PAGE_ID
import requests
from datetime import datetime, timedelta, UTC
from app.services.auth_meta_service import get_token_valido
from app.database import SessionLocal, obter_ultimo_numero_antes, salvar_numero_seguidores


def obter_token_pagina(access_token_usuario: str, page_id: str) -> str | None:
    print("[Facebook] Buscando token da página...")
    url = "https://graph.facebook.com/v17.0/me/accounts"
    params = {"access_token": access_token_usuario}
    resp = requests.get(url, params=params)

    print(f"[Facebook] Status response token página: {resp.status_code}")
    if resp.status_code != 200:
        print("Erro ao obter token da página:", resp.status_code, resp.text)
        return None

    contas = resp.json().get("data", [])
    print(f"[Facebook] Contas encontradas: {contas}")

    for pg in contas:
        if pg.get("id") == page_id:
            print(f"[Facebook] Página encontrada! Token: {pg.get('access_token')[:10]}...")
            return pg.get("access_token")

    print("Página não encontrada nos accounts.")
    return None


def obter_nome_pagina(page_id: str, token_pagina: str) -> str | None:
    print("[Facebook] Buscando nome da página...")
    url = f"https://graph.facebook.com/v17.0/{page_id}"
    params = {"fields": "name", "access_token": token_pagina}

    resp = requests.get(url, params=params)
    print(f"[Facebook] Status response nome página: {resp.status_code}")

    if resp.status_code != 200:
        print("Erro ao obter nome da página:", resp.status_code, resp.text)
        return None

    nome = resp.json().get("name")
    print(f"[Facebook] Nome da página: {nome}")
    return nome


def obter_numero_seguidores(page_id: str, token_pagina: str):
    print("[Facebook] Buscando número de seguidores...")
    url = f"https://graph.facebook.com/v17.0/{page_id}/insights/page_fans"
    resp = requests.get(url, params={"access_token": token_pagina})
    print(f"[Facebook] Status response seguidores: {resp.status_code}")

    if resp.status_code != 200:
        print("Erro ao obter seguidores:", resp.status_code, resp.text)
        return None

    data = resp.json().get("data", [])
    print(f"[Facebook] Dados de seguidores brutos: {data}")

    try:
        return data[0]["values"][-1]["value"]
    except Exception as e:
        print("Erro ao acessar valor de seguidores:", e)
        return None


def obter_publicacoes_semana(page_id: str, token_pagina: str, since: datetime, until: datetime):
    print("[Facebook] Buscando publicações da semana...")
    url = f"https://graph.facebook.com/v17.0/{page_id}/posts"
    params = {
        "access_token": token_pagina,
        "since": int(since.timestamp()),
        "until": int(until.timestamp()),
        "limit": 100
    }
    resp = requests.get(url, params=params)
    print(f"[Facebook] Status response posts: {resp.status_code}")

    if resp.status_code != 200:
        print("Erro ao obter posts:", resp.status_code, resp.text)
        return []

    posts = resp.json().get("data", [])
    print(f"[Facebook] {len(posts)} publicações encontradas")
    return posts


def obter_alcance_total(posts: list, token_pagina: str):
    total = 0
    for post in posts:
        resp = requests.get(
            f"https://graph.facebook.com/v17.0/{post['id']}/insights",
            params={"metric": "post_impressions_unique", "access_token": token_pagina}
        )
        if resp.status_code == 200:
            for item in resp.json().get("data", []):
                if item["name"] == "post_impressions_unique":
                    total += item["values"][0].get("value", 0)
    return total


def obter_engajamento_total(posts: list, token_pagina: str):
    total = 0
    for post in posts:
        resp = requests.get(
            f"https://graph.facebook.com/v17.0/{post['id']}/insights",
            params={"metric": "post_engaged_users", "access_token": token_pagina}
        )
        if resp.status_code == 200:
            for item in resp.json().get("data", []):
                if item["name"] == "post_engaged_users":
                    total += item["values"][0].get("value", 0)
    return total


def obter_relatorio_semanal_facebook():
    print("Iniciando geração de relatório semanal do Facebook...")
    db = SessionLocal()
    
    usuario_token = get_token_valido()
    if not usuario_token:
        print("Token de usuário inválido.")
        return {"erro": "Não foi possível obter token de usuário"}

    page_token = obter_token_pagina(usuario_token, FB_PAGE_ID)
    if not page_token:
        print("Token da página não encontrado.")
        return {"erro": "Não foi possível obter token da página"}

    page_id = FB_PAGE_ID
    page_nome = obter_nome_pagina(page_id, page_token)
    today = datetime.now(UTC)
    last_week = today - timedelta(days=7)

    seguidores_inicio = obter_ultimo_numero_antes(db, "facebook", page_id, last_week)
    seguidores_fim = obter_numero_seguidores(page_id, page_token)

    if seguidores_fim is not None:
        print(f"[Facebook] Salvando seguidores atuais: {seguidores_fim}")
        salvar_numero_seguidores(db, "facebook", page_id, page_nome, seguidores_fim, today)
    else:
        print("Seguidores fim está como None!")

    posts = obter_publicacoes_semana(page_id, page_token, last_week, today)
    alcance = obter_alcance_total(posts, page_token)
    engajamento = obter_engajamento_total(posts, page_token)
    engajamento_medio = (engajamento / alcance * 100) if alcance else 0

    print("✅ Relatório Facebook gerado com sucesso.")
    return {
        "rede_social": "Facebook",
        "seguidores_inicio": seguidores_inicio,
        "seguidores_fim": seguidores_fim,
        "publicacoes": len(posts),
        "alcance_total": alcance,
        "engajamento_medio": round(engajamento_medio, 2)
    }
