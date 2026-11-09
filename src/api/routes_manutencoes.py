import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List, Optional
from src.core.db import get_db
from src.core.config import UPLOADS_DIR
from src.repositories.repository import VehicleRepository
from src.models.schemas import (
    RegistroManutencaoResponse, ManutencaoCorretivaCreate, ComprovanteResponse
)

router = APIRouter(prefix="/api", tags=["Registros de Manutenção & Comprovantes"])

ALLOWED_MIMETYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "application/pdf": ".pdf"
}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

@router.get("/manutencoes", response_model=List[RegistroManutencaoResponse])
def list_manutencoes(veiculo_id: Optional[int] = None):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        return repo.list_manutencoes(veiculo_id)

@router.get("/manutencoes/{manutencao_id}", response_model=RegistroManutencaoResponse)
def get_manutencao(manutencao_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        m = repo.get_manutencao(manutencao_id)
        if not m:
            raise HTTPException(status_code=404, detail="Registro de manutenção não encontrado")
        return m

@router.post("/manutencoes/corretiva", response_model=RegistroManutencaoResponse, status_code=201)
def create_manutencao_corretiva(data: ManutencaoCorretivaCreate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(data.veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

        despesas_dicts = [d.model_dump() for d in data.despesas]
        manutencao_id = repo.create_manutencao(
            veiculo_id=data.veiculo_id,
            tipo_intervencao="CORRETIVA",
            titulo=data.titulo,
            odometro=data.odometro,
            data_execucao=data.data_execucao,
            oficina_local=data.oficina_local or "",
            observacoes=data.observacoes or "",
            despesas=despesas_dicts
        )

        # Atualiza odômetro se for maior
        if data.odometro > veic["odometro_referencia"]:
            repo.update_odometro(data.veiculo_id, data.odometro, "MANUTENCAO_CORRETIVA")

        return repo.get_manutencao(manutencao_id)

@router.post("/manutencoes/{manutencao_id}/anexos", response_model=ComprovanteResponse, status_code=201)
async def upload_comprovante(manutencao_id: int, file: UploadFile = File(...)):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        m = repo.get_manutencao(manutencao_id)
        if not m:
            raise HTTPException(status_code=404, detail="Registro de manutenção não encontrado")

        mimetype = file.content_type or "application/octet-stream"
        ext = ALLOWED_MIMETYPES.get(mimetype)
        if not ext:
            # Fallback para extensão pelo nome original
            orig_path = Path(file.filename)
            ext = orig_path.suffix.lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp", ".pdf"]:
                raise HTTPException(
                    status_code=400,
                    detail="Formato de arquivo não suportado. Envie imagens JPG, PNG, WEBP ou documentos PDF."
                )

        unique_name = f"{uuid.uuid4().hex}{ext}"
        destination = UPLOADS_DIR / unique_name

        # Lê e grava garantindo limite de tamanho
        total_size = 0
        with open(destination, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    buffer.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(status_code=400, detail="O arquivo excede o limite máximo permitido de 15 MB.")
                buffer.write(chunk)

        comprovante_id = repo.create_comprovante(
            manutencao_id=manutencao_id,
            filename=unique_name,
            original_name=file.filename or unique_name,
            filepath=str(destination),
            mimetype=mimetype,
            tamanho_bytes=total_size
        )
        return repo.get_comprovante(comprovante_id)

@router.get("/anexos/{comprovante_id}/download")
def download_comprovante(comprovante_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        comp = repo.get_comprovante(comprovante_id)
        if not comp:
            raise HTTPException(status_code=404, detail="Comprovante não encontrado")
        file_path = Path(comp["filepath"])
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo físico não encontrado no servidor")
        return FileResponse(
            path=str(file_path),
            media_type=comp["mimetype"],
            filename=comp["original_name"]
        )

@router.delete("/anexos/{comprovante_id}", status_code=204)
def delete_comprovante(comprovante_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        comp = repo.get_comprovante(comprovante_id)
        if not comp:
            raise HTTPException(status_code=404, detail="Comprovante não encontrado")
        file_path = Path(comp["filepath"])
        file_path.unlink(missing_ok=True)
        repo.delete_comprovante(comprovante_id)
        return None
