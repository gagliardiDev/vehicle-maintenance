import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any

class VehicleRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # --- VEÍCULOS ---
    def list_veiculos(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM veiculos ORDER BY id ASC")
        return [dict(row) for row in cursor.fetchall()]

    def get_veiculo(self, veiculo_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM veiculos WHERE id = ?", (veiculo_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def create_veiculo(self, nome: str, tipo: str, ano: int, placa: Optional[str], odometro: int) -> int:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            """INSERT INTO veiculos (nome, tipo, ano, placa, odometro_referencia, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nome, tipo, ano, placa, odometro, now, now)
        )
        veiculo_id = cursor.lastrowid
        self.add_odometro_historico(veiculo_id, odometro, "CADASTRO")
        return veiculo_id

    def update_odometro(self, veiculo_id: int, odometro: int, origem: str = "ATUALIZACAO_RAPIDA") -> bool:
        now = datetime.now().isoformat()
        self.conn.execute(
            "UPDATE veiculos SET odometro_referencia = ?, updated_at = ? WHERE id = ?",
            (odometro, now, veiculo_id)
        )
        self.add_odometro_historico(veiculo_id, odometro, origem)
        return True

    def add_odometro_historico(self, veiculo_id: int, odometro: int, origem: str):
        now = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO odometro_historico (veiculo_id, odometro, data_registro, origem) VALUES (?, ?, ?, ?)",
            (veiculo_id, odometro, now, origem)
        )

    def get_odometro_historico(self, veiculo_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM odometro_historico WHERE veiculo_id = ? ORDER BY id DESC LIMIT 50",
            (veiculo_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    # --- ITENS MONITORADOS ---
    def list_itens_by_veiculo(self, veiculo_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM itens_monitorados WHERE veiculo_id = ? ORDER BY id ASC",
            (veiculo_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM itens_monitorados WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def create_item(self, veiculo_id: int, nome: str, categoria: str, intervalo_km: Optional[int],
                    intervalo_meses: Optional[int], ultimo_odometro: int, ultima_data: str, observacoes: str = "") -> int:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            """INSERT INTO itens_monitorados 
               (veiculo_id, nome, categoria, intervalo_km, intervalo_meses, ultimo_odometro, ultima_data, observacoes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (veiculo_id, nome, categoria, intervalo_km, intervalo_meses, ultimo_odometro, ultima_data, observacoes, now)
        )
        return cursor.lastrowid

    def update_item(self, item_id: int, updates: Dict[str, Any]) -> bool:
        allowed = ["nome", "categoria", "intervalo_km", "intervalo_meses", "ultimo_odometro", "ultima_data", "observacoes"]
        fields = [f"{k} = ?" for k in updates if k in allowed]
        if not fields:
            return False
        values = [updates[k] for k in updates if k in allowed]
        values.append(item_id)
        self.conn.execute(f"UPDATE itens_monitorados SET {', '.join(fields)} WHERE id = ?", tuple(values))
        return True

    def update_item_ciclo(self, item_id: int, ultimo_odometro: int, ultima_data: str):
        self.conn.execute(
            "UPDATE itens_monitorados SET ultimo_odometro = ?, ultima_data = ? WHERE id = ?",
            (ultimo_odometro, ultima_data, item_id)
        )

    def delete_item(self, item_id: int) -> bool:
        self.conn.execute("DELETE FROM itens_monitorados WHERE id = ?", (item_id,))
        return True

    # --- REVISÕES PLANEJADAS ---
    def list_revisoes(self, veiculo_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM revisoes_planejadas WHERE 1=1"
        params = []
        if veiculo_id:
            query += " AND veiculo_id = ?"
            params.append(veiculo_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC"
        cursor = self.conn.execute(query, tuple(params))
        revisoes = [dict(r) for r in cursor.fetchall()]
        for rev in revisoes:
            rev["itens"] = self.get_revisao_itens(rev["id"])
        return revisoes

    def get_revisao(self, revisao_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM revisoes_planejadas WHERE id = ?", (revisao_id,))
        row = cursor.fetchone()
        if not row:
            return None
        rev = dict(row)
        rev["itens"] = self.get_revisao_itens(revisao_id)
        return rev

    def get_revisao_itens(self, revisao_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM revisao_itens WHERE revisao_id = ? ORDER BY tipo ASC, id ASC",
            (revisao_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    def create_revisao(self, veiculo_id: int, titulo: str, odometro_previsto: int,
                       data_prevista: Optional[str], observacoes: str, itens: List[Dict[str, Any]]) -> int:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            """INSERT INTO revisoes_planejadas (veiculo_id, titulo, odometro_previsto, data_prevista, status, observacoes, created_at)
               VALUES (?, ?, ?, ?, 'PLANEJADA', ?, ?)""",
            (veiculo_id, titulo, odometro_previsto, data_prevista, observacoes, now)
        )
        revisao_id = cursor.lastrowid
        for it in itens:
            self.conn.execute(
                """INSERT INTO revisao_itens 
                   (revisao_id, tipo, item_monitorado_id, descricao, part_number, fornecedor, quantidade, valor_estimado, comprado_porta_malas, executado)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)""",
                (revisao_id, it["tipo"], it.get("item_monitorado_id"), it["descricao"],
                 it.get("part_number"), it.get("fornecedor"), it.get("quantidade", 1.0),
                 it.get("valor_estimado", 0.0), 1 if it.get("comprado_porta_malas") else 0)
            )
        return revisao_id

    def toggle_porta_malas(self, revisao_item_id: int, comprado: bool) -> bool:
        self.conn.execute(
            "UPDATE revisao_itens SET comprado_porta_malas = ? WHERE id = ?",
            (1 if comprado else 0, revisao_item_id)
        )
        return True

    def set_revisao_status(self, revisao_id: int, status: str):
        self.conn.execute("UPDATE revisoes_planejadas SET status = ? WHERE id = ?", (status, revisao_id))

    # --- REGISTROS DE MANUTENÇÃO & DESPESAS ---
    def create_manutencao(self, veiculo_id: int, tipo_intervencao: str, titulo: str,
                          odometro: int, data_execucao: str, oficina_local: str,
                          observacoes: str, despesas: List[Dict[str, Any]],
                          revisao_planejada_id: Optional[int] = None) -> int:
        now = datetime.now().isoformat()
        total_pecas = sum(d.get("quantidade", 1.0) * d.get("valor_unitario", 0.0) for d in despesas if d.get("tipo") == "PECA")
        total_servicos = sum(d.get("quantidade", 1.0) * d.get("valor_unitario", 0.0) for d in despesas if d.get("tipo") == "SERVICO")
        total_geral = total_pecas + total_servicos

        cursor = self.conn.execute(
            """INSERT INTO registros_manutencao 
               (veiculo_id, revisao_planejada_id, tipo_intervencao, titulo, odometro, data_execucao, oficina_local,
                total_pecas, total_servicos, total_geral, observacoes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (veiculo_id, revisao_planejada_id, tipo_intervencao, titulo, odometro,
             data_execucao, oficina_local, total_pecas, total_servicos, total_geral, observacoes, now)
        )
        manutencao_id = cursor.lastrowid

        for d in despesas:
            qtd = d.get("quantidade", 1.0)
            val = d.get("valor_unitario", 0.0)
            self.conn.execute(
                """INSERT INTO despesas_itemizadas 
                   (manutencao_id, tipo, descricao, part_number, fornecedor, quantidade, valor_unitario, valor_total)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (manutencao_id, d["tipo"], d["descricao"], d.get("part_number"), d.get("fornecedor"), qtd, val, qtd * val)
            )
        return manutencao_id

    def list_manutencoes(self, veiculo_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM registros_manutencao WHERE 1=1"
        params = []
        if veiculo_id:
            query += " AND veiculo_id = ?"
            params.append(veiculo_id)
        query += " ORDER BY odometro DESC, data_execucao DESC, id DESC"
        cursor = self.conn.execute(query, tuple(params))
        manutencoes = [dict(r) for r in cursor.fetchall()]
        for m in manutencoes:
            m["despesas"] = self.get_despesas_by_manutencao(m["id"])
            m["comprovantes"] = self.get_comprovantes_by_manutencao(m["id"])
        return manutencoes

    def get_manutencao(self, manutencao_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM registros_manutencao WHERE id = ?", (manutencao_id,))
        row = cursor.fetchone()
        if not row:
            return None
        m = dict(row)
        m["despesas"] = self.get_despesas_by_manutencao(manutencao_id)
        m["comprovantes"] = self.get_comprovantes_by_manutencao(manutencao_id)
        return m

    def get_despesas_by_manutencao(self, manutencao_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM despesas_itemizadas WHERE manutencao_id = ? ORDER BY tipo ASC, id ASC",
            (manutencao_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    # --- COMPROVANTES ---
    def create_comprovante(self, manutencao_id: int, filename: str, original_name: str,
                           filepath: str, mimetype: str, tamanho_bytes: int) -> int:
        now = datetime.now().isoformat()
        cursor = self.conn.execute(
            """INSERT INTO comprovantes (manutencao_id, filename, original_name, filepath, mimetype, tamanho_bytes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (manutencao_id, filename, original_name, filepath, mimetype, tamanho_bytes, now)
        )
        return cursor.lastrowid

    def get_comprovantes_by_manutencao(self, manutencao_id: int) -> List[Dict[str, Any]]:
        cursor = self.conn.execute(
            "SELECT * FROM comprovantes WHERE manutencao_id = ? ORDER BY id DESC",
            (manutencao_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    def get_comprovante(self, comprovante_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM comprovantes WHERE id = ?", (comprovante_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def delete_comprovante(self, comprovante_id: int) -> bool:
        self.conn.execute("DELETE FROM comprovantes WHERE id = ?", (comprovante_id,))
        return True

    # --- RELATÓRIOS E DASHBOARD ---
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        c = self.conn.cursor()
        
        # Totais gerais
        c.execute("SELECT SUM(total_pecas), SUM(total_servicos), SUM(total_geral) FROM registros_manutencao")
        row = c.fetchone()
        total_pecas = row[0] or 0.0
        total_servicos = row[1] or 0.0
        total_geral = row[2] or 0.0

        pct_pecas = (total_pecas / total_geral * 100.0) if total_geral > 0 else 0.0
        pct_servicos = (total_servicos / total_geral * 100.0) if total_geral > 0 else 0.0

        # Gastos por veículo
        c.execute("""
            SELECT v.id, v.nome, 
                   COALESCE(SUM(m.total_geral), 0.0) as total_gasto,
                   COALESCE(SUM(m.total_pecas), 0.0) as total_pecas,
                   COALESCE(SUM(m.total_servicos), 0.0) as total_servicos,
                   COUNT(m.id) as total_manutencoes,
                   MIN(m.odometro) as min_km,
                   MAX(m.odometro) as max_km
            FROM veiculos v
            LEFT JOIN registros_manutencao m ON m.veiculo_id = v.id
            GROUP BY v.id
        """)
        veiculos_gastos = []
        for r in c.fetchall():
            tot = r["total_gasto"]
            min_k = r["min_km"]
            max_k = r["max_km"]
            custo_km = None
            if min_k is not None and max_k is not None and (max_k - min_k) > 0 and tot > 0:
                custo_km = round(tot / (max_k - min_k), 2)
            veiculos_gastos.append({
                "veiculo_id": r["id"],
                "veiculo_nome": r["nome"],
                "total_gasto": round(tot, 2),
                "total_pecas": round(r["total_pecas"], 2),
                "total_servicos": round(r["total_servicos"], 2),
                "total_manutencoes": r["total_manutencoes"],
                "custo_por_km": custo_km
            })

        # Gastos mensais (últimos 12 meses agrupados por YYYY-MM)
        c.execute("""
            SELECT SUBSTR(data_execucao, 1, 7) as mes,
                   SUM(total_geral) as total,
                   SUM(total_pecas) as total_pecas,
                   SUM(total_servicos) as total_servicos
            FROM registros_manutencao
            WHERE data_execucao IS NOT NULL AND data_execucao != ''
            GROUP BY SUBSTR(data_execucao, 1, 7)
            ORDER BY mes ASC
        """)
        gastos_mensais = [
            {
                "mes": r["mes"],
                "total": round(r["total"], 2),
                "total_pecas": round(r["total_pecas"], 2),
                "total_servicos": round(r["total_servicos"], 2)
            }
            for r in c.fetchall()
        ]

        # Contadores rápidos
        c.execute("SELECT COUNT(*) FROM veiculos")
        tot_veic = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM revisoes_planejadas WHERE status = 'PLANEJADA'")
        tot_rev_plan = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM registros_manutencao")
        tot_manut = c.fetchone()[0]

        return {
            "total_geral_gasto": round(total_geral, 2),
            "proporcao": {
                "total_pecas": round(total_pecas, 2),
                "total_servicos": round(total_servicos, 2),
                "percentual_pecas": round(pct_pecas, 1),
                "percentual_servicos": round(pct_servicos, 1)
            },
            "gastos_por_veiculo": veiculos_gastos,
            "gastos_mensais": gastos_mensais,
            "total_veiculos": tot_veic,
            "total_revisoes_planejadas": tot_rev_plan,
            "total_manutencoes_feitas": tot_manut
        }
