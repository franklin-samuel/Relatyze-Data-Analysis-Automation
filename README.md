# 📊 Relatyze | Análise de Dados e Automação - Sistema de Relatórios Semanais

https://relatyze-data-analysis-automation.onrender.com/docs (Versão inicial da API com apenas Youtube, Facebook e Instagram rodando na nuvem) -> Integrando com o frontend...

## ✨ Visão Geral

Este sistema tem como objetivo automatizar a geração de relatórios semanais de desempenho de contas em redes sociais. O usuário poderá:

- Integrar com APIs oficiais (Instagram, Facebook, Threads, YouTube, TikTok)
- Inserir dados manualmente (Kwai)
- Visualizar relatórios semanais detalhados
- Publicar vídeos automaticamente em múltiplas redes sociais com um único upload (funcionalidade futura)

---

## 🧠 Funcionalidades

- 📈 Geração de relatórios semanais por rede social
- 🔌 Integração com APIs externas:
  - Instagram/Facebook (Meta Graph API)
  - YouTube Shorts (YouTube Data API)
  - Threads (Threads API)
  - TikTok (TikTok API)
- 📝 Inserção manual de dados para plataformas sem API:
  - Kwai
- 🧾 Relatórios incluem:
  - Seguidores (início e fim da semana)
  - Total de publicações
  - Alcance total
  - Engajamento médio (%)
- 📤 Upload de vídeo único e publicação automática em múltiplas redes (🚧 futura implementação)

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Linguagem:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de Dados:** PostgreSQL
- **Autenticação com Google e Meta (OAuth 2.0)**
- **Nuvem(Render)**

### Frontend
- **Plataforma:** React Native Web (via Expo Web)
- **Interface para Web:** Expo + JavaScript/TypeScript

---

## 📦 Status Atual
- ⏳ Criando o frontend e conectando a nossa API locada na nuvem(Render)
  

---

## 👨‍💻 Desenvolvedor

- [@franklin-samuel](https://github.com/franklin-samuel)
