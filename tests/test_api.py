import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_read_dashboard():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Mercado 2 Irmãos" in response.text

def test_api_kpis():
    with TestClient(app) as client:
        response = client.get("/api/kpis")
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas_faturamento" in data
        assert "ticket_medio" in data

def test_api_vendas_diarias():
    with TestClient(app) as client:
        response = client.get("/api/vendas-diarias")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_api_top_produtos():
    with TestClient(app) as client:
        response = client.get("/api/top-produtos?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 5

