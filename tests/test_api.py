import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.core.db import init_db, get_db
from src.services.seed_data import seed_initial_data
import src.core.config as config

@pytest.fixture(scope="module")
def client():
    # Cria banco temporário para testes
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        test_db_path = tmp.name

    original_db_path = config.DB_PATH
    config.DB_PATH = Path(test_db_path)

    init_db(test_db_path)
    with get_db(test_db_path) as conn:
        seed_initial_data(conn)

    with TestClient(app) as test_client:
        yield test_client

    # Cleanup
    try:
        os.remove(test_db_path)
    except Exception:
        pass
    config.DB_PATH = original_db_path

def test_healthcheck(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_seed_veiculos(client):
    response = client.get("/api/veiculos")
    assert response.status_code == 200
    veiculos = response.json()
    assert len(veiculos) >= 2
    
    sx4 = next(v for v in veiculos if "SX4" in v["nome"])
    biz = next(v for v in veiculos if "Biz" in v["nome"])

    assert sx4["odometro_referencia"] == 101000
    assert sx4["tipo"] == "CARRO"
    assert biz["tipo"] == "MOTO"
    assert biz["odometro_referencia"] == 0

def test_atualizacao_rapida_odometro(client):
    response = client.get("/api/veiculos")
    biz = next(v for v in response.json() if "Biz" in v["nome"])
    biz_id = biz["id"]

    # Atualiza KM da Biz para 45.200
    res_up = client.post(f"/api/veiculos/{biz_id}/odometro", json={"odometro": 45200})
    assert res_up.status_code == 200
    assert res_up.json()["odometro_referencia"] == 45200

    # Tenta diminuir odômetro -> Erro 400
    res_bad = client.post(f"/api/veiculos/{biz_id}/odometro", json={"odometro": 40000})
    assert res_bad.status_code == 400

    # Verifica histórico de odômetro
    res_hist = client.get(f"/api/veiculos/{biz_id}/odometro/historico")
    assert res_hist.status_code == 200
    historico = res_hist.json()
    assert len(historico) >= 2
    assert historico[0]["odometro"] == 45200
    assert historico[0]["origem"] == "ATUALIZACAO_RAPIDA"

def test_plano_preventivo_gatilho_hibrido(client):
    response = client.get("/api/veiculos")
    sx4 = next(v for v in response.json() if "SX4" in v["nome"])
    sx4_id = sx4["id"]

    res_itens = client.get(f"/api/veiculos/{sx4_id}/itens")
    assert res_itens.status_code == 200
    itens = res_itens.json()
    assert len(itens) >= 10

    # Óleo do motor do SX4 (trocado aos 92k km, carro está com 101k km -> rodou 9k de 10k km e passou 12 meses -> status deve ser VENCIDO por tempo ou PROXIMO por km)
    it_oleo = next(i for i in itens if "Óleo do Motor" in i["nome"])
    assert it_oleo["status_vencimento"] in ["PROXIMO", "VENCIDO"]
    assert it_oleo["km_restante"] == 1000  # (92000 + 10000) - 101000 = 1000

    # Velas iridium (trocadas aos 87k km com intervalo de 60k km -> alvo 147k km)
    it_velas = next(i for i in itens if "Velas de Ignição" in i["nome"])
    assert it_velas["status_vencimento"] == "EM_DIA"
    assert it_velas["proximo_odometro_alvo"] == 147000
    assert it_velas["km_restante"] == 46000

def test_revisao_planejada_e_checklist_porta_malas(client):
    response = client.get("/api/veiculos")
    sx4 = next(v for v in response.json() if "SX4" in v["nome"])
    
    res_revs = client.get(f"/api/revisoes?veiculo_id={sx4['id']}")
    assert res_revs.status_code == 200
    revisoes = res_revs.json()
    assert len(revisoes) >= 1
    
    rev_101k = revisoes[0]
    assert rev_101k["status"] == "PLANEJADA"
    assert len(rev_101k["itens"]) > 0

    # Localiza o filtro de ar no checklist
    item_filtro_ar = next(i for i in rev_101k["itens"] if "Filtro de Ar" in i["descricao"])
    assert item_filtro_ar["comprado_porta_malas"] is False

    # Marca como "Comprado / No porta-malas"
    res_toggle = client.patch(
        f"/api/revisoes/itens/{item_filtro_ar['id']}/porta-malas",
        json={"comprado": True}
    )
    assert res_toggle.status_code == 200
    assert res_toggle.json()["comprado"] is True

    # Recarrega revisão e checa contador de porta-malas
    res_updated = client.get(f"/api/revisoes/{rev_101k['id']}")
    assert res_updated.status_code == 200
    assert res_updated.json()["total_porta_malas"] >= 1

def test_conclusao_revisao_atomica(client):
    response = client.get("/api/veiculos")
    sx4 = next(v for v in response.json() if "SX4" in v["nome"])
    res_revs = client.get(f"/api/revisoes?veiculo_id={sx4['id']}&status=PLANEJADA")
    rev = res_revs.json()[0]

    # Conclui a revisão na oficina aos 101.200 km com peças e mão de obra
    payload = {
        "odometro_real": 101200,
        "data_execucao": "2026-11-10",
        "oficina_local": "Oficina Mecânica SX4 Express",
        "observacoes": "Revisão dos 101k concluída com sucesso. TBI e MAF limpos.",
        "despesas": [
            {
                "tipo": "PECA",
                "item_monitorado_id": None,
                "descricao": "Filtro de Ar Wega",
                "part_number": "JFA 0885",
                "fornecedor": "Mercado Livre",
                "quantidade": 1.0,
                "valor_unitario": 55.0
            },
            {
                "tipo": "PECA",
                "item_monitorado_id": None,
                "descricao": "Óleo 5W-30 Sintético (4.5L)",
                "part_number": "5W30 SP",
                "fornecedor": "Oficina",
                "quantidade": 4.5,
                "valor_unitario": 50.0
            },
            {
                "tipo": "SERVICO",
                "item_monitorado_id": None,
                "descricao": "Mão de Obra Troca de Óleo e Filtros",
                "part_number": None,
                "fornecedor": "Oficina",
                "quantidade": 1.0,
                "valor_unitario": 80.0
            }
        ]
    }

    res_concluir = client.post(f"/api/revisoes/{rev['id']}/concluir", json=payload)
    assert res_concluir.status_code == 200
    manutencao = res_concluir.json()
    assert manutencao["total_pecas"] == (55.0 + 4.5 * 50.0)  # 280.0
    assert manutencao["total_servicos"] == 80.0
    assert manutencao["total_geral"] == 360.0

    # Verifica se o odômetro do SX4 atualizou para 101.200 km
    res_sx4 = client.get(f"/api/veiculos/{sx4['id']}")
    assert res_sx4.json()["odometro_referencia"] == 101200

    # Verifica se a revisão agora está CONCLUIDA
    res_rev_check = client.get(f"/api/revisoes/{rev['id']}")
    assert res_rev_check.json()["status"] == "CONCLUIDA"

def test_manutencao_corretiva_avulsa(client):
    response = client.get("/api/veiculos")
    biz = next(v for v in response.json() if "Biz" in v["nome"])

    payload = {
        "veiculo_id": biz["id"],
        "titulo": "Conserto Pneu Furado e Troca de Câmara Traseira",
        "odometro": 45300,
        "data_execucao": "2026-11-12",
        "oficina_local": "Borracharia São Cristóvão",
        "observacoes": "Prego na roda traseira na avenida principal.",
        "despesas": [
            {
                "tipo": "PECA",
                "descricao": "Câmara de Ar Traseira Rinaldi",
                "part_number": "Cam-14",
                "fornecedor": "Borracharia",
                "quantidade": 1.0,
                "valor_unitario": 35.0
            },
            {
                "tipo": "SERVICO",
                "descricao": "Remoção, Montagem e Balanceamento Manual",
                "part_number": None,
                "fornecedor": "Borracharia",
                "quantidade": 1.0,
                "valor_unitario": 20.0
            }
        ]
    }

    res = client.post("/api/manutencoes/corretiva", json=payload)
    assert res.status_code == 201
    corretiva = res.json()
    assert corretiva["tipo_intervencao"] == "CORRETIVA"
    assert corretiva["total_pecas"] == 35.0
    assert corretiva["total_servicos"] == 20.0
    assert corretiva["total_geral"] == 55.0

def test_comprovante_upload_e_download(client):
    response = client.get("/api/manutencoes")
    assert response.status_code == 200
    manutencoes = response.json()
    assert len(manutencoes) > 0
    manutencao_id = manutencoes[0]["id"]

    # Cria arquivo fictício para upload
    fake_content = b"%PDF-1.4 dummy pdf content for receipt"
    files = {"file": ("nota_fiscal_oficina.pdf", fake_content, "application/pdf")}

    res_upload = client.post(f"/api/manutencoes/{manutencao_id}/anexos", files=files)
    assert res_upload.status_code == 201
    comprovante = res_upload.json()
    assert comprovante["original_name"] == "nota_fiscal_oficina.pdf"
    assert comprovante["mimetype"] == "application/pdf"
    comp_id = comprovante["id"]

    # Testa download do comprovante
    res_down = client.get(f"/api/anexos/{comp_id}/download")
    assert res_down.status_code == 200
    assert res_down.content == fake_content

    # Testa remoção do comprovante
    res_del = client.delete(f"/api/anexos/{comp_id}")
    assert res_del.status_code == 204

    # Verifica que foi excluído
    res_down_after = client.get(f"/api/anexos/{comp_id}/download")
    assert res_down_after.status_code == 404

def test_dashboard_relatorios(client):
    res = client.get("/api/relatorios/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert data["total_geral_gasto"] > 0
    assert data["proporcao"]["total_pecas"] > 0
    assert data["proporcao"]["total_servicos"] > 0
    assert len(data["gastos_por_veiculo"]) >= 2
    assert len(data["gastos_mensais"]) > 0
