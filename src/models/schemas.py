from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class TipoVeiculo(str, Enum):
    CARRO = "CARRO"
    MOTO = "MOTO"

class StatusVencimento(str, Enum):
    EM_DIA = "EM_DIA"
    PROXIMO = "PROXIMO"
    VENCIDO = "VENCIDO"

class StatusRevisao(str, Enum):
    PLANEJADA = "PLANEJADA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

class TipoDespesa(str, Enum):
    PECA = "PECA"
    SERVICO = "SERVICO"

class TipoIntervencao(str, Enum):
    PREVENTIVA = "PREVENTIVA"
    CORRETIVA = "CORRETIVA"
    INSPECAO = "INSPECAO"

# Veículos
class VeiculoBase(BaseModel):
    nome: str
    tipo: TipoVeiculo
    ano: int
    placa: Optional[str] = None
    odometro_referencia: int = Field(default=0, ge=0)

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(BaseModel):
    nome: Optional[str] = None
    ano: Optional[int] = None
    placa: Optional[str] = None

class OdometroUpdate(BaseModel):
    odometro: int = Field(..., ge=0)

class OdometroHistoricoResponse(BaseModel):
    id: int
    veiculo_id: int
    odometro: int
    data_registro: str
    origem: str

class VeiculoResponse(VeiculoBase):
    id: int
    itens_vencidos: int = 0
    itens_proximos: int = 0
    created_at: str
    updated_at: str

# Itens Monitorados
class ItemMonitoradoBase(BaseModel):
    nome: str
    categoria: str
    intervalo_km: Optional[int] = None
    intervalo_meses: Optional[int] = None
    ultimo_odometro: int = 0
    ultima_data: str
    observacoes: Optional[str] = ""

class ItemMonitoradoCreate(ItemMonitoradoBase):
    veiculo_id: int

class ItemMonitoradoUpdate(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    intervalo_km: Optional[int] = None
    intervalo_meses: Optional[int] = None
    ultimo_odometro: Optional[int] = None
    ultima_data: Optional[str] = None
    observacoes: Optional[str] = None

class ItemMonitoradoResponse(ItemMonitoradoBase):
    id: int
    veiculo_id: int
    km_restante: Optional[int] = None
    dias_restantes: Optional[int] = None
    proximo_odometro_alvo: Optional[int] = None
    proxima_data_alvo: Optional[str] = None
    status_vencimento: StatusVencimento
    percentual_km: Optional[float] = None
    percentual_tempo: Optional[float] = None
    created_at: str

# Revisões Planejadas
class RevisaoItemCreate(BaseModel):
    tipo: TipoDespesa
    item_monitorado_id: Optional[int] = None
    descricao: str
    part_number: Optional[str] = None
    fornecedor: Optional[str] = None
    quantidade: float = 1.0
    valor_estimado: float = 0.0
    comprado_porta_malas: bool = False

class RevisaoItemResponse(BaseModel):
    id: int
    revisao_id: int
    tipo: TipoDespesa
    item_monitorado_id: Optional[int] = None
    descricao: str
    part_number: Optional[str] = None
    fornecedor: Optional[str] = None
    quantidade: float
    valor_estimado: float
    comprado_porta_malas: bool
    executado: bool

class RevisaoPlanejadaCreate(BaseModel):
    veiculo_id: int
    titulo: str
    odometro_previsto: int
    data_prevista: Optional[str] = None
    observacoes: Optional[str] = ""
    itens: List[RevisaoItemCreate] = []

class RevisaoPlanejadaResponse(BaseModel):
    id: int
    veiculo_id: int
    titulo: str
    odometro_previsto: int
    data_prevista: Optional[str] = None
    status: StatusRevisao
    observacoes: Optional[str] = None
    created_at: str
    itens: List[RevisaoItemResponse] = []
    total_estimado: float = 0.0
    total_porta_malas: int = 0
    total_itens_pecas: int = 0

class ConcluirRevisaoItemReal(BaseModel):
    tipo: TipoDespesa
    item_monitorado_id: Optional[int] = None
    descricao: str
    part_number: Optional[str] = None
    fornecedor: Optional[str] = None
    quantidade: float = 1.0
    valor_unitario: float = 0.0

class ConcluirRevisaoRequest(BaseModel):
    odometro_real: int
    data_execucao: str
    oficina_local: Optional[str] = ""
    observacoes: Optional[str] = ""
    despesas: List[ConcluirRevisaoItemReal] = []

# Registros de Manutenção e Despesas
class DespesaItemizadaCreate(BaseModel):
    tipo: TipoDespesa
    descricao: str
    part_number: Optional[str] = None
    fornecedor: Optional[str] = None
    quantidade: float = 1.0
    valor_unitario: float = 0.0

class DespesaItemizadaResponse(BaseModel):
    id: int
    manutencao_id: int
    tipo: TipoDespesa
    descricao: str
    part_number: Optional[str] = None
    fornecedor: Optional[str] = None
    quantidade: float
    valor_unitario: float
    valor_total: float

class ComprovanteResponse(BaseModel):
    id: int
    manutencao_id: int
    filename: str
    original_name: str
    mimetype: str
    tamanho_bytes: int
    created_at: str

class ManutencaoCorretivaCreate(BaseModel):
    veiculo_id: int
    titulo: str
    odometro: int
    data_execucao: str
    oficina_local: Optional[str] = ""
    observacoes: Optional[str] = ""
    despesas: List[DespesaItemizadaCreate] = []

class RegistroManutencaoResponse(BaseModel):
    id: int
    veiculo_id: int
    revisao_planejada_id: Optional[int] = None
    tipo_intervencao: TipoIntervencao
    titulo: str
    odometro: int
    data_execucao: str
    oficina_local: Optional[str] = None
    total_pecas: float
    total_servicos: float
    total_geral: float
    observacoes: Optional[str] = None
    created_at: str
    despesas: List[DespesaItemizadaResponse] = []
    comprovantes: List[ComprovanteResponse] = []

# Relatórios e Dashboard
class GastoMensalItem(BaseModel):
    mes: str  # YYYY-MM
    total: float
    total_pecas: float
    total_servicos: float

class GastoPorVeiculoItem(BaseModel):
    veiculo_id: int
    veiculo_nome: str
    total_gasto: float
    total_pecas: float
    total_servicos: float
    total_manutencoes: int
    custo_por_km: Optional[float] = None

class ProporcaoDespesa(BaseModel):
    total_pecas: float
    total_servicos: float
    percentual_pecas: float
    percentual_servicos: float

class DashboardSummaryResponse(BaseModel):
    total_geral_gasto: float
    proporcao: ProporcaoDespesa
    gastos_por_veiculo: List[GastoPorVeiculoItem]
    gastos_mensais: List[GastoMensalItem]
    total_veiculos: int
    total_revisoes_planejadas: int
    total_manutencoes_feitas: int
