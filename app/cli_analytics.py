from app.database.connection import SessionLocal
from app.repositories.venda_repository import VendaRepository, init_db
from app.services.analytics_service import AnalyticsService

def main():
    init_db()
    session = SessionLocal()
    try:
        repo = VendaRepository(session)
        repo.carregar_e_popular_json("bdados_venda.json")
        analytics = AnalyticsService(session)

        kpis = analytics.obter_resumo_kpis()
        top_produtos = analytics.obter_top_produtos_vendidos(limit=5)
        
        print("\n==============================================")
        print("  📊 MERCADO 2 IRMÃOS - DASHBOARD ANALÍTICO")
        print("==============================================")
        print(f"💰 Faturamento Total:   R$ {kpis['total_vendas_faturamento']:.2f}")
        print(f"🛒 Qtd de Vendas:       {kpis['quantidade_vendas']}")
        print(f"🏷️ Ticket Médio:         R$ {kpis['ticket_medio']:.2f}")
        print(f"📅 Média Diária:        R$ {kpis['media_diaria']:.2f} (em {kpis['dias_com_venda']} dias)")
        
        print("\n🏆 Top 5 Produtos por Faturamento:")
        print("----------------------------------------------")
        for idx, item in enumerate(top_produtos, 1):
            print(f" {idx}. {item['produto']:<30} | Qtd: {item['quantidade_vendida']:<3} | R$ {item['faturamento']:.2f}")
        print("==============================================\n")
    finally:
        session.close()

if __name__ == "__main__":
    main()
