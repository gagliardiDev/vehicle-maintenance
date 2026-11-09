from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from src.core.db import get_db
from src.repositories.repository import VehicleRepository
from src.services.maintenance_service import MaintenanceService
from src.models.schemas import (
    RevisaoPlanejadaResponse, RevisaoPlanejadaCreate, ConcluirRevisaoRequest,
    RegistroManutencaoResponse
)

router = APIRouter(prefix="/api/revisoes", tags=["Revisões Planejadas"])

class TogglePortaMalasBody(BaseModel):
    comprado: bool

def enrich_revisao(r: dict) -> dict:
    itens = r.get("itens", [])
    total_est = sum(it.get("quantidade", 1.0) * it.get("valor_estimado", 0.0) for it in itens)
    total_pm = sum(1 for it in itens if it.get("comprado_porta_malas") and it.get("tipo") == "PECA")
    total_pecas = sum(1 for it in itens if it.get("tipo") == "PECA")
    res = dict(r)
    res["total_estimado"] = round(total_est, 2)
    res["total_porta_malas"] = total_pm
    res["total_itens_pecas"] = total_pecas
    return res

@router.get("", response_model=List[RevisaoPlanejadaResponse])
def list_revisoes(veiculo_id: Optional[int] = None, status: Optional[str] = None):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        revisoes = repo.list_revisoes(veiculo_id, status)
        return [enrich_revisao(r) for r in revisoes]

@router.get("/{revisao_id}", response_model=RevisaoPlanejadaResponse)
def get_revisao(revisao_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        r = repo.get_revisao(revisao_id)
        if not r:
            raise HTTPException(status_code=404, detail="Revisão não encontrada")
        return enrich_revisao(r)

@router.post("", response_model=RevisaoPlanejadaResponse, status_code=201)
def create_revisao(data: RevisaoPlanejadaCreate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(data.veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        itens_dict = [it.model_dump() for it in data.itens]
        revisao_id = repo.create_revisao(
            veiculo_id=data.veiculo_id,
            titulo=data.titulo,
            odometro_previsto=data.odometro_previsto,
            data_prevista=data.data_prevista,
            observacoes=data.observacoes or "",
            itens=itens_dict
        )
        r = repo.get_revisao(revisao_id)
        return enrich_revisao(r)

@router.patch("/itens/{revisao_item_id}/porta-malas")
def toggle_porta_malas(revisao_item_id: int, body: TogglePortaMalasBody):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        repo.toggle_porta_malas(revisao_item_id, body.comprado)
        return {"success": True, "revisao_item_id": revisao_item_id, "comprado": body.comprado}

@router.post("/{revisao_id}/concluir", response_model=RegistroManutencaoResponse)
def concluir_revisao(revisao_id: int, data: ConcluirRevisaoRequest):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        service = MaintenanceService(repo)
        try:
            despesas_dicts = [d.model_dump() for d in data.despesas]
            manutencao_id = service.concluir_revisao(
                revisao_id=revisao_id,
                odometro_real=data.odometro_real,
                data_execucao=data.data_execucao,
                oficina_local=data.oficina_local or "",
                observacoes=data.observacoes or "",
                despesas_reais=despesas_dicts
            )
            return repo.get_manutencao(manutencao_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/{revisao_id}/cancelar")
def cancelar_revisao(revisao_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        r = repo.get_revisao(revisao_id)
        if not r:
            raise HTTPException(status_code=404, detail="Revisão não encontrada")
        repo.set_revisao_status(revisao_id, "CANCELADA")
        return {"success": True, "revisao_id": revisao_id, "status": "CANCELADA"}
