import pytest
from app.database.connection import Base, engine, SessionLocal
from app.repositories.venda_repository import VendaRepository
from app.services.analytics_service import AnalyticsService

@pytest.fixture
def db_populated():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    repo = VendaRepository(session)
    repo.carregar_e_popular_json("bdados_venda.json")
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_obter_resumo_kpis(db_populated):
    analytics = AnalyticsService(db_populated)
    kpis = analytics.obter_resumo_kpis()
    
    assert kpis["quantidade_vendas"] == 31
    assert kpis["total_vendas_faturamento"] > 0
    assert kpis["ticket_medio"] > 0
    assert kpis["dias_com_venda"] > 0

def test_obter_vendas_diarias(db_populated):
    analytics = AnalyticsService(db_populated)
    vendas_diarias = analytics.obter_vendas_diarias()
    
    assert len(vendas_diarias) > 0
    assert "data" in vendas_diarias[0]
    assert "total_vendido" in vendas_diarias[0]

def test_obter_top_produtos(db_populated):
    analytics = AnalyticsService(db_populated)
    top_prods = analytics.obter_top_produtos_vendidos(limit=5)
    
    assert len(top_prods) == 5
    assert "produto" in top_prods[0]
    assert "faturamento" in top_prods[0]
