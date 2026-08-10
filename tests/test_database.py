import os
import pytest
from app.database.connection import Base, engine, SessionLocal
from app.repositories.venda_repository import VendaRepository
from app.models.entities import Venda, Produto

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_popular_banco_dados(db_session):
    repo = VendaRepository(db_session)
    json_path = "bdados_venda.json"
    
    assert os.path.exists(json_path)
    inseridas = repo.carregar_e_popular_json(json_path)
    assert inseridas > 0

    vendas = repo.listar_todas()
    assert len(vendas) == inseridas
    
    total = repo.obter_total_vendas()
    assert total > 0

