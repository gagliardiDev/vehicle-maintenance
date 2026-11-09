from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.core.db import get_db
from src.repositories.repository import VehicleRepository
from src.services.maintenance_service import MaintenanceService
from src.models.schemas import (
    VeiculoResponse, VeiculoCreate, VeiculoUpdate, OdometroUpdate,
    OdometroHistoricoResponse, ItemMonitoradoResponse, ItemMonitoradoCreate, ItemMonitoradoUpdate
)

router = APIRouter(prefix="/api", tags=["Veículos & Odometria"])

@router.get("/veiculos", response_model=List[VeiculoResponse])
def list_veiculos():
    with get_db() as conn:
        service = MaintenanceService(VehicleRepository(conn))
        return service.list_veiculos_com_contadores()

@router.get("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def get_veiculo(veiculo_id: int):
    with get_db() as conn:
        service = MaintenanceService(VehicleRepository(conn))
        veic = service.get_veiculo_com_contadores(veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        return veic

@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def create_veiculo(data: VeiculoCreate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veiculo_id = repo.create_veiculo(
            nome=data.nome,
            tipo=data.tipo.value,
            ano=data.ano,
            placa=data.placa,
            odometro=data.odometro_referencia
        )
        service = MaintenanceService(repo)
        return service.get_veiculo_com_contadores(veiculo_id)

@router.put("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def update_veiculo(veiculo_id: int, data: VeiculoUpdate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        if updates:
            fields = [f"{k} = ?" for k in updates]
            values = list(updates.values()) + [veiculo_id]
            conn.execute(f"UPDATE veiculos SET {', '.join(fields)} WHERE id = ?", tuple(values))
        service = MaintenanceService(repo)
        return service.get_veiculo_com_contadores(veiculo_id)

@router.post("/veiculos/{veiculo_id}/odometro", response_model=VeiculoResponse)
def update_odometro(veiculo_id: int, data: OdometroUpdate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        if data.odometro < veic["odometro_referencia"]:
            raise HTTPException(
                status_code=400,
                detail=f"O novo odômetro ({data.odometro} km) não pode ser inferior ao odômetro atual ({veic['odometro_referencia']} km)."
            )
        repo.update_odometro(veiculo_id, data.odometro, origem="ATUALIZACAO_RAPIDA")
        service = MaintenanceService(repo)
        return service.get_veiculo_com_contadores(veiculo_id)

@router.get("/veiculos/{veiculo_id}/odometro/historico", response_model=List[OdometroHistoricoResponse])
def get_odometro_historico(veiculo_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        return repo.get_odometro_historico(veiculo_id)

# Itens Monitorados do Veículo
@router.get("/veiculos/{veiculo_id}/itens", response_model=List[ItemMonitoradoResponse])
def list_itens_veiculo(veiculo_id: int):
    with get_db() as conn:
        service = MaintenanceService(VehicleRepository(conn))
        return service.list_itens_calculados(veiculo_id)

@router.post("/veiculos/{veiculo_id}/itens", response_model=ItemMonitoradoResponse, status_code=201)
def create_item(veiculo_id: int, data: ItemMonitoradoCreate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        veic = repo.get_veiculo(veiculo_id)
        if not veic:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        item_id = repo.create_item(
            veiculo_id=veiculo_id,
            nome=data.nome,
            categoria=data.categoria,
            intervalo_km=data.intervalo_km,
            intervalo_meses=data.intervalo_meses,
            ultimo_odometro=data.ultimo_odometro,
            ultima_data=data.ultima_data,
            observacoes=data.observacoes or ""
        )
        item = repo.get_item(item_id)
        service = MaintenanceService(repo)
        return service.calculate_item_status(item, veic["odometro_referencia"])

@router.put("/itens/{item_id}", response_model=ItemMonitoradoResponse)
def update_item(item_id: int, data: ItemMonitoradoUpdate):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        item = repo.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item monitorado não encontrado")
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        repo.update_item(item_id, updates)
        item_atualizado = repo.get_item(item_id)
        veic = repo.get_veiculo(item_atualizado["veiculo_id"])
        service = MaintenanceService(repo)
        return service.calculate_item_status(item_atualizado, veic["odometro_referencia"])

@router.delete("/itens/{item_id}", status_code=204)
def delete_item(item_id: int):
    with get_db() as conn:
        repo = VehicleRepository(conn)
        item = repo.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item monitorado não encontrado")
        repo.delete_item(item_id)
        return None
