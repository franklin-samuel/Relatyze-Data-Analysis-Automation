from TikTokApi import TikTokApi
from datetime import datetime, timedelta, UTC
from app.database import SessionLocal, obter_ultimo_numero_antes, salvar_numero_seguidores


def obter_relatorio_semanal_tiktok(username: str = "tiktok"):
    print(f"[TikTok] Gerando relatório semanal para @{username}")
    today = datetime.now(UTC)
    last_week = today - timedelta(days=7)

    try:
        with TikTokApi() as api:
            user = api.user(username=username)
            user_info = user.info()

            seguidores_fim = user_info['userInfo']['stats']['followerCount']
            perfil_id = user_info['userInfo']['user']['id']
            perfil_nome = user_info['userInfo']['user']['nickname']

            db = SessionLocal()
            seguidores_inicio = obter_ultimo_numero_antes(db, "tiktok", perfil_id, last_week)
            salvar_numero_seguidores(db, "tiktok", perfil_id, perfil_nome, seguidores_fim, today)

            posts = []
            for video in user.videos(count=50):
                create_time = datetime.fromtimestamp(video.as_dict['createTime'], tz=UTC)
                if last_week <= create_time <= today:
                        posts.append(video)
            
            alcance_total = sum(p.as_dict['stats']['playCount'] for p in posts)
            engajamento_total = sum(
                    p.as_dict['stats']['diggCount'] +
                    p.as_dict['stats']['shareCount'] +
                    p.as_dict['stats']['commentCount']
                    for p in posts
                )
            engajamento_medio = (engajamento_total / alcance_total * 100) if alcance_total else 0

            print(f"✅ Relatório Tiktok gerado com sucesso.")

            return {
                    "rede_social": "TikTok",
                    "seguidores_inicio": seguidores_inicio,
                    "seguidores_fim": seguidores_fim,
                    "publicacoes": len(posts),
                    "alcance_total": alcance_total,
                    "engajamento_medio": round(engajamento_medio, 2)
                }

    except Exception as e:
            print(f"[TikTok] Erro ao coletar dados: {e}")
            return {"erro": str(e)}