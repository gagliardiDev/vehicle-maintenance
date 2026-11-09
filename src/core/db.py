import sqlite3
from typing import Generator
from contextlib import contextmanager
from src.core import config

def get_db_connection(db_file: str = None) -> sqlite3.Connection:
    target = db_file or str(config.DB_PATH)
    conn = sqlite3.connect(target, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

@contextmanager
def get_db(db_file: str = None) -> Generator[sqlite3.Connection, None, None]:
    conn = get_db_connection(db_file)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db(db_file: str = None):
    with get_db(db_file) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('CARRO', 'MOTO')),
            ano INTEGER NOT NULL,
            placa TEXT,
            odometro_referencia INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS odometro_historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
            odometro INTEGER NOT NULL,
            data_registro TEXT NOT NULL,
            origem TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS itens_monitorados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            intervalo_km INTEGER,
            intervalo_meses INTEGER,
            ultimo_odometro INTEGER NOT NULL DEFAULT 0,
            ultima_data TEXT NOT NULL,
            observacoes TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS revisoes_planejadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
            titulo TEXT NOT NULL,
            odometro_previsto INTEGER NOT NULL,
            data_prevista TEXT,
            status TEXT NOT NULL DEFAULT 'PLANEJADA' CHECK(status IN ('PLANEJADA', 'CONCLUIDA', 'CANCELADA')),
            observacoes TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS revisao_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            revisao_id INTEGER NOT NULL REFERENCES revisoes_planejadas(id) ON DELETE CASCADE,
            tipo TEXT NOT NULL CHECK(tipo IN ('PECA', 'SERVICO')),
            item_monitorado_id INTEGER REFERENCES itens_monitorados(id) ON DELETE SET NULL,
            descricao TEXT NOT NULL,
            part_number TEXT,
            fornecedor TEXT,
            quantidade REAL NOT NULL DEFAULT 1.0,
            valor_estimado REAL NOT NULL DEFAULT 0.0,
            comprado_porta_malas INTEGER NOT NULL DEFAULT 0,
            executado INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS registros_manutencao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL REFERENCES veiculos(id) ON DELETE CASCADE,
            revisao_planejada_id INTEGER REFERENCES revisoes_planejadas(id) ON DELETE SET NULL,
            tipo_intervencao TEXT NOT NULL CHECK(tipo_intervencao IN ('PREVENTIVA', 'CORRETIVA', 'INSPECAO')),
            titulo TEXT NOT NULL,
            odometro INTEGER NOT NULL,
            data_execucao TEXT NOT NULL,
            oficina_local TEXT,
            total_pecas REAL NOT NULL DEFAULT 0.0,
            total_servicos REAL NOT NULL DEFAULT 0.0,
            total_geral REAL NOT NULL DEFAULT 0.0,
            observacoes TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS despesas_itemizadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manutencao_id INTEGER NOT NULL REFERENCES registros_manutencao(id) ON DELETE CASCADE,
            tipo TEXT NOT NULL CHECK(tipo IN ('PECA', 'SERVICO')),
            descricao TEXT NOT NULL,
            part_number TEXT,
            fornecedor TEXT,
            quantidade REAL NOT NULL DEFAULT 1.0,
            valor_unitario REAL NOT NULL DEFAULT 0.0,
            valor_total REAL NOT NULL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS comprovantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manutencao_id INTEGER NOT NULL REFERENCES registros_manutencao(id) ON DELETE CASCADE,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            filepath TEXT NOT NULL,
            mimetype TEXT NOT NULL,
            tamanho_bytes INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
