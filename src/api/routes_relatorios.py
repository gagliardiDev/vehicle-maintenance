from fastapi import APIRouter
from src.core.db import get_db
from src.repositories.repository import VehicleRepository
from src.models.schemas import DashboardSummaryResponse

router = APIRouter(prefix="/api/relatorios", tags=["Relatórios & Dashboard"])

@router.get("/dashboard", response_model=DashboardSummaryResponse)
def get_dashboard():
    with get_db() as conn:
        repo = VehicleRepository(conn)
        return repo.get_dashboard_metrics()
