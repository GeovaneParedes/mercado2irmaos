from app.database.connection import SessionLocal
from app.repositories.venda_repository import VendaRepository

def main():
    print("🚀 Carregando dados do bdados_venda.json para o banco SQLite...")
    session = SessionLocal()
    try:
        repo = VendaRepository(session)
        inseridas = repo.carregar_e_popular_json("bdados_venda.json")
        total = repo.obter_total_vendas()
        print(f"✅ Carga concluída com sucesso! Vendas processadas: {inseridas}")
        print(f"💰 Valor Acumulado Total em Banco: R$ {total:.2f}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
