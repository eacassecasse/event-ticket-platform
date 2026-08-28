import httpx
from contextlib import asynccontextmanager
from app.api.routes.auth import router as auth_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.events import router as events_router
from app.api.routes.payments import router as payments_router
from app.api.routes.reservations import (
    router as reservations_router,
)
from app.api.routes.tickets import (
    router as tickets_router,
)
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0)
        )

    yield

    await app.state.http_client.aclose()

app = FastAPI(
    title="Plataforma de Eventos e Ingressos",
    version="0.1.0",
    description="Plataforma de gestão de eventos e ingressos desenvolvida para o desafio Elite Dev.",
    lifespan=lifespan
)


app.include_router(
    auth_router,
    prefix='/api/v1'
)

app.include_router(
    catalog_router,
    prefix='/api/v1'
)

app.include_router(
    events_router,
    prefix='/api/v1'
)

app.include_router(
    reservations_router,
    prefix='/api/v1'
)

app.include_router(
    payments_router,
    prefix='/api/v1'
)

app.include_router(
    tickets_router,
    prefix="/api/v1",
)

@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
