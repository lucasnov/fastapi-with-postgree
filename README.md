
# Projeto Cloud - FastAPI e PostgreSQL

API RESTful que oferece:

* **Registro de Usuário** (`POST /registrar`)
* **Autenticação** – JWT (`POST /login`)
* **Consulta de Dados** via *scraping* das últimas 10 notícias do site Hacker News (`GET /consultar`)
* **Health‑check** (`GET /health-check`)

Todo o ambiente roda em contêineres Docker usando **Docker Compose**.

---

## Requisitos

* Docker **20.10+** (inclui Compose V2)

---

## 🏃‍♂️ Execução rápida

```bash
# 1 – Clone o repositório
git clone https://github.com/lucasnov/fastapi-with-postgree.git
cd fastapi-with-postgree   # execute tudo daqui

# 2 – Copie e edite variáveis de ambiente
cp .env.example .env
#   edite .env se quiser mudar usuário/senha do Postgres ou chave JWT

# 3 – Suba a stack
docker compose pull          # baixa imagens do Docker Hub
docker compose up -d         # sobe API + banco de dados

# 4 – Verifique
curl http://localhost:8000/health-check
```

> **Derrubar serviços:** `docker compose down`  
> **Logs em tempo real:** `docker compose logs -f`

---

## Endpoints principais

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `POST` | `/registrar` | Cria usuário | — |
| `POST` | `/login` | Retorna JWT | — |
| `GET`  | `/consultar` | Lista dados das últimas 10 notícias do site Hacker News | ✅ Bearer |
| `GET`  | `/health-check` | Status da API | — |

A documentação Swagger/OAS é servida em **`/docs`**.

---

## Como funciona

1. **PostgreSQL** é iniciado com usuário/senha definidos em `.env`.  
2. Ao subir, a API cria as tabelas (SQLAlchemy) e fica escutando na porta **8000**.  
3. Requests externos chegam diretamente ao contêiner `app` graças ao mapeamento `8000:8000` no Compose.

---

## Teste rápido (cURL)

```bash
# registrar
curl -X POST http://localhost:8000/registrar      -H "Content-Type: application/json"      -d '{"name":"Lucas","email":"lucas@example.com","password":"123456"}'

# login
TOKEN=$(curl -s -X POST http://localhost:8000/login                -H "Content-Type: application/json"                -d '{"email":"lucas@example.com","password":"123456"}'         | jq -r .access_token)

# consultar com JWT
curl -H "Authorization: Bearer $TOKEN"      http://localhost:8000/consultar
```

---
