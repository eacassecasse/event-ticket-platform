from fastapi import FastAPI

app = FastAPI(
    title="Plataforma de Eventos e Ingressos",
    version="0.1.0",
    description="Plataforma de gestão de eventos e ingressos desenvolvida para o desafio Elite Dev.",
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}