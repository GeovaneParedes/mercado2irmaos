from typing import Dict, Any, List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.entities import Venda, ItemVenda, Produto

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def obter_resumo_kpis(self) -> Dict[str, Any]:
        """Retorna os principais KPIs do negócio."""
        vendas = self.db.query(Venda).all()
        if not vendas:
            return {
                "total_vendas_faturamento": 0.0,
                "quantidade_vendas": 0,
                "ticket_medio": 0.0,
                "media_diaria": 0.0
            }

        faturamento_total = sum(v.valor_total for v in vendas)
        qtd_vendas = len(vendas)
        ticket_medio = faturamento_total / qtd_vendas if qtd_vendas > 0 else 0.0

        # Dias únicos de vendas
        dias_unicos = len(set(v.data.date() for v in vendas))
        media_diaria = faturamento_total / dias_unicos if dias_unicos > 0 else 0.0

        return {
            "total_vendas_faturamento": round(faturamento_total, 2),
            "quantidade_vendas": qtd_vendas,
            "ticket_medio": round(ticket_medio, 2),
            "media_diaria": round(media_diaria, 2),
            "dias_com_venda": dias_unicos
        }

    def obter_vendas_diarias(self) -> List[Dict[str, Any]]:
        """Retorna a série temporal de vendas agrupadas por dia."""
        resultados = (
            self.db.query(
                func.date(Venda.data).label("data_dia"),
                func.sum(Venda.valor_total).label("total_dia"),
                func.count(Venda.id).label("qtd_vendas")
            )
            .group_by(func.date(Venda.data))
            .order_by(func.date(Venda.data))
            .all()
        )
        return [
            {
                "data": str(r.data_dia),
                "total_vendido": round(float(r.total_dia), 2),
                "quantidade_vendas": int(r.qtd_vendas)
            }
            for r in resultados
        ]

    def obter_top_produtos_vendidos(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retorna os produtos mais vendidos por faturamento e quantidade."""
        resultados = (
            self.db.query(
                Produto.nome,
                func.sum(ItemVenda.quantidade).label("qtd_total"),
                func.sum(ItemVenda.quantidade * ItemVenda.preco_unitario).label("faturamento_produto")
            )
            .join(ItemVenda, Produto.id == ItemVenda.produto_id)
            .group_by(Produto.id, Produto.nome)
            .order_by(func.sum(ItemVenda.quantidade * ItemVenda.preco_unitario).desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "produto": r.nome,
                "quantidade_vendida": int(r.qtd_total),
                "faturamento": round(float(r.faturamento_produto), 2)
            }
            for r in resultados
        ]
