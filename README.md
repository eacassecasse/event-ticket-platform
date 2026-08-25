# Plataforma de Eventos e Ingressos

Plataforma full-stack para descoberta de eventos, reservas, pagamentos simulados, emissão de ingressos digitais e validação de entradas.

## Funcionalidades

- autenticação e autorização com JWT;
- catálogo de eventos, incluindo integração opcional com a Ticketmaster;
- gestão de eventos;
- reservas de lugares;
- pagamentos simulados;
- emissão e validação de ingressos.

## Tecnologias

- **Frontend:** React 19, TypeScript e Vite;
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy e Alembic;
- **Base de dados:** PostgreSQL 17;
- **Gestão de dependências:** pnpm e uv;
- **Infraestrutura local:** Docker Compose.

## Pré-requisitos

- Node.js 20+;
- pnpm 10+;
- Python 3.12+;
- [uv](https://docs.astral.sh/uv/);
- Docker e Docker Compose.

## Como executar

### 1. Instalar dependências do frontend

Na raiz do projecto:

```bash
pnpm install
```

### 2. Preparar a base de dados

```bash
docker compose -f infrastructure/compose/docker-compose.dev.yml up -d postgres
```

O serviço fica disponível em `localhost:5432` com a seguinte configuração:

| Parâmetro | Valor |
| --- | --- |
| Base de dados | `event_platform` |
| Utilizador | `postgres_usr` |
| Palavra-passe | `postgres_pwd` |

### 3. Configurar e iniciar o backend

```bash
cd apps/server
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

O backend fica disponível em `http://localhost:8000`.

- Health check: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`

Preencha `TICKETMASTER_API_KEY` no ficheiro `.env` caso pretenda activar a integração com a Ticketmaster. Em ambientes reais, substitua também os segredos e credenciais de desenvolvimento.

### 4. Iniciar o frontend

Noutro terminal, a partir da raiz:

```bash
pnpm --filter client dev
```

O frontend fica disponível em `http://localhost:5173`.

## Validação local

```bash
# Frontend
pnpm --filter client lint
pnpm --filter client build

# Backend
cd apps/server
uv run ruff check .
```

O backend inclui dependências de teste, mas ainda não existem testes automatizados no repositório.

## Estrutura

```text
apps/
├── client/       # Aplicação React
└── server/       # API FastAPI, domínio e migrações
docs/             # Documentação técnica
infrastructure/   # Docker Compose para desenvolvimento
specs/            # Requisitos funcionais
```

## Parar os serviços

```bash
docker compose -f infrastructure/compose/docker-compose.dev.yml down
```

Para remover também os dados persistidos do PostgreSQL:

```bash
docker compose -f infrastructure/compose/docker-compose.dev.yml down -v
```

## Melhorias recomendadas

1. Adicionar testes unitários, de integração e end-to-end aos fluxos críticos.
2. Implementar CI/CD com lint, type checking, testes, build e análise de segurança.
3. Criar uma configuração de produção com gestão segura de segredos, CORS restrito e observabilidade.
4. Adicionar Redis para expiração de reservas e tarefas assíncronas.
5. Completar o frontend com integração da API, tratamento de erros e estados de carregamento.
6. Documentar contratos da API, estratégia de versionamento e fluxo de deploy.

## Contribuição

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para as convenções de branches, commits e Pull Requests. A documentação adicional está disponível em [docs/](docs/) e os requisitos funcionais em [specs/](specs/).

## Licença

Consulte [LICENSE](LICENSE).
