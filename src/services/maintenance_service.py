from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from src.repositories.repository import VehicleRepository
from src.models.schemas import StatusVencimento

class MaintenanceService:
    def __init__(self, repo: VehicleRepository):
        self.repo = repo

    def calculate_item_status(self, item: Dict[str, Any], odometro_referencia: int) -> Dict[str, Any]:
        result = dict(item)
        intervalo_km = item.get("intervalo_km")
        intervalo_meses = item.get("intervalo_meses")
        ultimo_odometro = item.get("ultimo_odometro") or 0
        ultima_data_str = item.get("ultima_data")
        
        today = date.today()
        km_restante = None
        dias_restantes = None
        proximo_odometro_alvo = None
        proxima_data_alvo_str = None
        pct_km = None
        pct_tempo = None

        # Cálculo de KM
        if intervalo_km is not None and intervalo_km > 0:
            proximo_odometro_alvo = ultimo_odometro + intervalo_km
            km_restante = proximo_odometro_alvo - odometro_referencia
            km_rodado = max(0, odometro_referencia - ultimo_odometro)
            pct_km = min(100.0, round((km_rodado / intervalo_km) * 100.0, 1))

        # Cálculo de Tempo
        if intervalo_meses is not None and intervalo_meses > 0 and ultima_data_str:
            try:
                dt_ultima = datetime.strptime(ultima_data_str[:10], "%Y-%m-%d").date()
                dias_intervalo = int(intervalo_meses * 30.4375)
                proxima_data = dt_ultima + timedelta(days=dias_intervalo)
                proxima_data_alvo_str = proxima_data.isoformat()
                dias_restantes = (proxima_data - today).days
                dias_decorridos = max(0, (today - dt_ultima).days)
                pct_tempo = min(100.0, round((dias_decorridos / dias_intervalo) * 100.0, 1))
            except Exception:
                pass

        # Determinação do Status de Vencimento (o critério mais restritivo prevalece)
        is_vencido = False
        is_proximo = False

        if km_restante is not None and km_restante <= 0:
            is_vencido = True
        if dias_restantes is not None and dias_restantes <= 0:
            is_vencido = True

        if not is_vencido:
            if km_restante is not None and km_restante <= 1000:
                is_proximo = True
            if dias_restantes is not None and dias_restantes <= 30:
                is_proximo = True

        if is_vencido:
            status = StatusVencimento.VENCIDO
        elif is_proximo:
            status = StatusVencimento.PROXIMO
        else:
            status = StatusVencimento.EM_DIA

        result["km_restante"] = km_restante
        result["dias_restantes"] = dias_restantes
        result["proximo_odometro_alvo"] = proximo_odometro_alvo
        result["proxima_data_alvo"] = proxima_data_alvo_str
        result["status_vencimento"] = status
        result["percentual_km"] = pct_km
        result["percentual_tempo"] = pct_tempo

        return result

    def get_veiculo_com_contadores(self, veiculo_id: int) -> Optional[Dict[str, Any]]:
        veiculo = self.repo.get_veiculo(veiculo_id)
        if not veiculo:
            return None
        
        itens = self.repo.list_itens_by_veiculo(veiculo_id)
        vencidos = 0
        proximos = 0
        for it in itens:
            calc = self.calculate_item_status(it, veiculo["odometro_referencia"])
            if calc["status_vencimento"] == StatusVencimento.VENCIDO:
                vencidos += 1
            elif calc["status_vencimento"] == StatusVencimento.PROXIMO:
                proximos += 1

        res = dict(veiculo)
        res["itens_vencidos"] = vencidos
        res["itens_proximos"] = proximos
        return res

    def list_veiculos_com_contadores(self) -> List[Dict[str, Any]]:
        veiculos = self.repo.list_veiculos()
        result = []
        for v in veiculos:
            v_calc = self.get_veiculo_com_contadores(v["id"])
            if v_calc:
                result.append(v_calc)
        return result

    def list_itens_calculados(self, veiculo_id: int) -> List[Dict[str, Any]]:
        veiculo = self.repo.get_veiculo(veiculo_id)
        if not veiculo:
            return []
        itens = self.repo.list_itens_by_veiculo(veiculo_id)
        return [self.calculate_item_status(it, veiculo["odometro_referencia"]) for it in itens]

    def concluir_revisao(self, revisao_id: int, odometro_real: int, data_execucao: str,
                         oficina_local: str, observacoes: str, despesas_reais: List[Dict[str, Any]]) -> int:
        revisao = self.repo.get_revisao(revisao_id)
        if not revisao:
            raise ValueError("Revisão planejada não encontrada")
        if revisao["status"] == "CONCLUIDA":
            raise ValueError("Esta revisão já foi concluída anteriormente")

        veiculo_id = revisao["veiculo_id"]
        veiculo = self.repo.get_veiculo(veiculo_id)
        if not veiculo:
            raise ValueError("Veículo não encontrado")

        # 1. Cria o registro de manutenção com despesas
        manutencao_id = self.repo.create_manutencao(
            veiculo_id=veiculo_id,
            tipo_intervencao="PREVENTIVA",
            titulo=revisao["titulo"],
            odometro=odometro_real,
            data_execucao=data_execucao,
            oficina_local=oficina_local or "Oficina Mecânica",
            observacoes=observacoes or revisao.get("observacoes", ""),
            despesas=despesas_reais,
            revisao_planejada_id=revisao_id
        )

        # 2. Atualiza status da revisão planejada para CONCLUIDA
        self.repo.set_revisao_status(revisao_id, "CONCLUIDA")

        # 3. Atualiza o odômetro do veículo se odometro_real for maior
        if odometro_real > veiculo["odometro_referencia"]:
            self.repo.update_odometro(veiculo_id, odometro_real, f"MANUTENCAO_REV_{revisao_id}")

        # 4. Atualiza os ciclos dos itens monitorados vinculados
        for desp in despesas_reais:
            it_id = desp.get("item_monitorado_id")
            if it_id:
                self.repo.update_item_ciclo(it_id, odometro_real, data_execucao)

        return manutencao_id
