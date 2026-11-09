import sqlite3
from src.repositories.repository import VehicleRepository

def seed_initial_data(conn: sqlite3.Connection):
    repo = VehicleRepository(conn)
    veiculos = repo.list_veiculos()
    if veiculos:
        # Já populado, não duplica
        return

    # --- 1. SUZUKI SX4 ---
    sx4_id = repo.create_veiculo(
        nome="Suzuki SX4 2.0 16V 4WD",
        tipo="CARRO",
        ano=2011,
        placa="SX4-4WD",
        odometro=101000
    )

    # Itens preventivos do SX4
    it_oleo = repo.create_item(sx4_id, "Óleo do Motor 5W-30 Sintético", "MOTOR", 10000, 6, 92000, "2025-11-01", "Óleo 5W-30 100% Sintético API SP / ILSAC GF-6A (4,5 Litros)")
    it_foleo = repo.create_item(sx4_id, "Filtro de Óleo do Motor", "MOTOR", 10000, 6, 92000, "2025-11-01", "Modelos Mahle OC 534, Mann W610/83, Hengst H97W07 + Arruela M14")
    it_far = repo.create_item(sx4_id, "Filtro de Ar do Motor", "AR_E_FILTROS", 15000, 12, 87000, "2025-05-15", "Wega JFA 0885, Tecfil ARL 7714 ou Japanparts FA8306S")
    it_fcabine = repo.create_item(sx4_id, "Filtro de Cabine / Ar-Condicionado", "AR_E_FILTROS", 15000, 12, 87000, "2025-05-15", "Tecfil ACP 709, Wega AKX 1965 ou Mahle LA 301")
    it_dif = repo.create_item(sx4_id, "Óleo Diferencial Traseiro e Transferência", "TRANSMISSAO", 40000, 24, 60000, "2024-05-10", "API GL-5 SAE 80W-90 ou 75W-90 (0,8L traseiro + 0,6L transferência = ~1,4L)")
    repo.create_item(sx4_id, "Óleo do Câmbio Automático", "TRANSMISSAO", 40000, 36, 87000, "2025-05-15", "Fluido ATF Suzuki 3317 ou Mobil 3309 (próxima troca prevista para ~130.000 km)")
    repo.create_item(sx4_id, "Velas de Ignição (Iridium)", "MOTOR", 60000, 48, 87000, "2025-05-15", "Velas NGK Iridium IFR6J11 (durabilidade de até ~150.000 km)")
    repo.create_item(sx4_id, "Correia de Acessórios (Poly-V)", "MOTOR", 40000, 36, 87000, "2025-05-15", "Correia Poly-V Contitech / Gates (próxima troca prevista para ~130.000 km)")
    repo.create_item(sx4_id, "Fluido de Freio (DOT 4)", "FREIOS", 20000, 24, 87000, "2025-05-15", "Fluido sintético DOT 4 de alto ponto de ebulição")
    repo.create_item(sx4_id, "Pastilhas de Freio Dianteiras", "FREIOS", 25000, 24, 92000, "2025-11-01", "Pastilhas cerâmicas / semimetálicas dianteiras")

    # Histórico do SX4 aos 87.000 km
    repo.create_manutencao(
        veiculo_id=sx4_id,
        tipo_intervencao="PREVENTIVA",
        titulo="Revisão dos 87.000 km (Aquisição do Carro)",
        odometro=87000,
        data_execucao="2025-05-15",
        oficina_local="Oficina Especializada",
        observacoes="Revisão geral completa logo após aquisição do veículo aos 87k km.",
        despesas=[
            {"tipo": "PECA", "descricao": "Óleo 5W-30 Sintético (4,5L) + Filtro de Óleo", "part_number": "OC 534", "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 230.0},
            {"tipo": "PECA", "descricao": "Filtro de Ar do Motor", "part_number": "JFA 0885", "fornecedor": "Mercado Livre", "quantidade": 1.0, "valor_unitario": 55.0},
            {"tipo": "PECA", "descricao": "Filtro de Cabine / Ar-Condicionado", "part_number": "ACP 709", "fornecedor": "Mercado Livre", "quantidade": 1.0, "valor_unitario": 45.0},
            {"tipo": "PECA", "descricao": "Jogo de Velas Iridium (4 un.)", "part_number": "IFR6J11", "fornecedor": "Autopeças", "quantidade": 1.0, "valor_unitario": 320.0},
            {"tipo": "PECA", "descricao": "Fluido de Câmbio ATF", "part_number": "Mobil 3309", "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 360.0},
            {"tipo": "PECA", "descricao": "Correia de Acessórios Poly-V", "part_number": "Gates 5PK", "fornecedor": "Autopeças", "quantidade": 1.0, "valor_unitario": 120.0},
            {"tipo": "PECA", "descricao": "Fluido de Freio DOT 4", "part_number": "Varga DOT4", "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 70.0},
            {"tipo": "PECA", "descricao": "Kit Amortecedor Dianteiro + Coifa LE", "part_number": "Kit Diant", "fornecedor": "Autopeças", "quantidade": 1.0, "valor_unitario": 480.0},
            {"tipo": "SERVICO", "descricao": "Mão de Obra Revisão Geral + Suspensão Dianteira", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 450.0}
        ]
    )

    # Histórico do SX4 aos 92.000 km
    repo.create_manutencao(
        veiculo_id=sx4_id,
        tipo_intervencao="PREVENTIVA",
        titulo="Revisão dos 92.000 km (Troca de Óleo por Tempo)",
        odometro=92000,
        data_execucao="2025-11-01",
        oficina_local="Oficina Mecânica",
        observacoes="Troca preventiva de óleo por atingir 6 meses, bateria nova e freios dianteiros.",
        despesas=[
            {"tipo": "PECA", "descricao": "Óleo 5W-30 Sintético (4,5L) + Filtro", "part_number": "OC 534", "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 240.0},
            {"tipo": "PECA", "descricao": "Pastilhas de Freio Dianteiras", "part_number": "Cobreq N-1480", "fornecedor": "Autopeças", "quantidade": 1.0, "valor_unitario": 180.0},
            {"tipo": "PECA", "descricao": "Bateria 60 Ah Selada", "part_number": "Moura 60Ah", "fornecedor": "Casa das Baterias", "quantidade": 1.0, "valor_unitario": 460.0},
            {"tipo": "SERVICO", "descricao": "Mão de Obra Troca Pastilhas e Filtro", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_unitario": 90.0},
            {"tipo": "SERVICO", "descricao": "Geometria (Alinhamento 3D) e Balanceamento de Rodas", "part_number": None, "fornecedor": "Centro Automotivo", "quantidade": 1.0, "valor_unitario": 120.0}
        ]
    )

    # Revisão Planejada dos 101.000 km do SX4
    repo.create_revisao(
        veiculo_id=sx4_id,
        titulo="Revisão dos 101.000 km (Fluidos, Filtros e Injeção)",
        odometro_previsto=101000,
        data_prevista="2026-11-15",
        observacoes="Comprar filtros e óleo GL-5 antecipadamente para levar no porta-malas. Executar troca de óleo 5W-30 e limpezas na oficina.",
        itens=[
            # Peças para levar no porta-malas
            {"tipo": "PECA", "item_monitorado_id": it_far, "descricao": "Filtro de Ar do Motor", "part_number": "Wega JFA 0885 / Tecfil ARL 7714", "fornecedor": "Mercado Livre", "quantidade": 1.0, "valor_estimado": 55.0, "comprado_porta_malas": False},
            {"tipo": "PECA", "item_monitorado_id": it_fcabine, "descricao": "Filtro de Cabine / Ar-Condicionado", "part_number": "Tecfil ACP 709 / Mahle LA 301", "fornecedor": "Mercado Livre", "quantidade": 1.0, "valor_estimado": 45.0, "comprado_porta_malas": False},
            {"tipo": "PECA", "item_monitorado_id": it_dif, "descricao": "Óleo Diferencial e Transferência (2 Litros)", "part_number": "API GL-5 SAE 80W-90 ou 75W-90", "fornecedor": "Autopeças Web", "quantidade": 2.0, "valor_estimado": 65.0, "comprado_porta_malas": False},
            # Serviços e peças da oficina
            {"tipo": "PECA", "item_monitorado_id": it_oleo, "descricao": "Óleo do Motor 5W-30 100% Sintético (4,5 L)", "part_number": "API SP / ILSAC GF-6A", "fornecedor": "Oficina", "quantidade": 4.5, "valor_estimado": 50.0, "comprado_porta_malas": False},
            {"tipo": "PECA", "item_monitorado_id": it_foleo, "descricao": "Filtro de Óleo do Motor + Arruela Vedação M14", "part_number": "OC 534 / H97W07", "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 45.0, "comprado_porta_malas": False},
            {"tipo": "SERVICO", "item_monitorado_id": None, "descricao": "Instalação do Filtro de Ar e Cabine (Peças no porta-malas)", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 40.0, "comprado_porta_malas": False},
            {"tipo": "SERVICO", "item_monitorado_id": it_dif, "descricao": "Troca de Óleo Diferencial Traseiro (~0,8L) e Caixa Transferência (~0,6L)", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 90.0, "comprado_porta_malas": False},
            {"tipo": "SERVICO", "item_monitorado_id": None, "descricao": "Limpeza Sensor MAF (Spray Limpa Contatos) + Corpo de Borboleta (TBI) e Válvula PCV", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 160.0, "comprado_porta_malas": False},
            {"tipo": "SERVICO", "item_monitorado_id": None, "descricao": "Rodízio de Pneus, Geometria (Alinhamento) e Balanceamento", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 130.0, "comprado_porta_malas": False},
            {"tipo": "SERVICO", "item_monitorado_id": None, "descricao": "Inspeção Visual Preventiva no Elevador (Tampa radiador 1.1 bar, fluido arrefecimento, coifa LD, buchas)", "part_number": None, "fornecedor": "Oficina", "quantidade": 1.0, "valor_estimado": 0.0, "comprado_porta_malas": False}
        ]
    )

    # --- 2. HONDA BIZ 125 2011 ---
    biz_id = repo.create_veiculo(
        nome="Honda Biz 125 2011",
        tipo="MOTO",
        ano=2011,
        placa="BIZ-125",
        odometro=0  # Provisório pós-retífica do motor, ajustável via Atualização Rápida
    )

    # Itens preventivos da Biz
    repo.create_item(biz_id, "Troca de Óleo do Motor (10W-30)", "MOTOR", 1500, 6, 0, "2026-10-01", "Óleo 10W-30 Semissintético ou Mineral JASO MA (~0,7L a 0,8L)")
    repo.create_item(biz_id, "Lubrificação e Tensão da Corrente", "CORRENTE_RELACAO", 500, 1, 0, "2026-10-01", "Checar folga da corrente (20-30mm) e lubrificar com óleo SAE 80/90 ou spray")
    repo.create_item(biz_id, "Kit Relação (Corrente, Coroa e Pinhão)", "CORRENTE_RELACAO", 15000, 24, 0, "2026-10-01", "Kit relação reforçado com retentor (DID / KMC / Riffel)")
    repo.create_item(biz_id, "Vela de Ignição", "MOTOR", 8000, 12, 0, "2026-10-01", "Vela NGK CPR6EA-9S ou CPR7EA-9")
    repo.create_item(biz_id, "Filtro de Ar", "AR_E_FILTROS", 4000, 12, 0, "2026-10-01", "Elemento filtrante de ar da Biz 125")
    repo.create_item(biz_id, "Lonas / Pastilhas de Freio", "FREIOS", 6000, 12, 0, "2026-10-01", "Verificação de desgaste das sapatas/lonas traseiras e dianteiras")
