import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.core.config import STATIC_DIR, HOST, PORT
from src.core.db import init_db, get_db
from src.services.seed_data import seed_initial_data
from src.api.routes_veiculos import router as veiculos_router
from src.api.routes_revisoes import router as revisoes_router
from src.api.routes_manutencoes import router as manutencoes_router
from src.api.routes_relatorios import router as relatorios_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inicializa DB e seed
    init_db()
    with get_db() as conn:
        seed_initial_data(conn)
    yield
    # Shutdown

app = FastAPI(
    title="Vehicle Maintenance API",
    description="Sistema de Controle de Manutenção Veicular e Gestão de Custos",
    version="1.0.0",
    lifespan=lifespan
)

# CORS liberado para rede local e dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas da API
app.include_router(veiculos_router)
app.include_router(revisoes_router)
app.include_router(manutencoes_router)
app.include_router(relatorios_router)

# Healthcheck
@app.get("/api/health")
def healthcheck():
    return {"status": "ok", "app": "vehicle-maintenance", "version": "1.0.0"}

# Serve frontend compilado caso exista
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Se for chamada de API não encontrada, deixa 404
        if full_path.startswith("api"):
            return FileResponse(status_code=404)
        file_candidate = STATIC_DIR / full_path
        if file_candidate.is_file():
            return FileResponse(file_candidate)
        return FileResponse(STATIC_DIR / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=False)
