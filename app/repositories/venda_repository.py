import json
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.entities import Venda, Produto, ItemVenda
from app.database.connection import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)

class VendaRepository:
    def __init__(self, db: Session):
        self.db = db

    def carregar_e_popular_json(self, json_path: str) -> int:
        """Lê o arquivo bdados_venda.json e insere no banco SQLite com tratamento de duplicatas."""
        init_db()
        with open(json_path, "r", encoding="utf-8") as f:
            vendas_data = json.load(f)

        vendas_inseridas = 0
        for item in vendas_data:
            # Verifica se a venda já existe no banco
            existing_venda = self.db.query(Venda).filter(Venda.id_venda_original == item["id_venda"]).first()
            if existing_venda:
                continue

            data_dt = datetime.strptime(item["data"], "%Y-%m-%d")
            nova_venda = Venda(
                id_venda_original=item["id_venda"],
                data=data_dt,
                valor_total=item["valor_total"]
            )
            self.db.add(nova_venda)
            self.db.flush()

            for prod in item["produtos"]:
                # Busca ou cria o produto
                produto = self.db.query(Produto).filter(Produto.nome == prod["nome"]).first()
                if not produto:
                    produto = Produto(
                        nome=prod["nome"],
                        preco_unitario=prod["preco_unitario"]
                    )
                    self.db.add(produto)
                    self.db.flush()

                item_venda = ItemVenda(
                    venda_id=nova_venda.id,
                    produto_id=produto.id,
                    quantidade=prod["quantidade"],
                    preco_unitario=prod["preco_unitario"]
                )
                self.db.add(item_venda)

            vendas_inseridas += 1

        self.db.commit()
        return vendas_inseridas

    def listar_todas(self) -> List[Venda]:
        return self.db.query(Venda).all()

    def obter_total_vendas(self) -> float:
        vendas = self.db.query(Venda).all()
        return sum(v.valor_total for v in vendas)
