from app.services.instagram_service import obter_relatorio_semanal_instagram
from app.services.facebook_service import obter_relatorio_semanal_facebook
from app.services.youtube_service import obter_relatorio_semanal_youtube
from app.services.tiktok_service import obter_relatorio_semanal_tiktok

def coletar_relatorio_geral():
    instagram = obter_relatorio_semanal_instagram()
    facebook = obter_relatorio_semanal_facebook()
    youtube = obter_relatorio_semanal_youtube()
    tiktok = obter_relatorio_semanal_tiktok("saopaulofc")

    return {
        "instagram": instagram,
        "facebook": facebook,
        "youtube": youtube,
        "tiktok": tiktok
    }

