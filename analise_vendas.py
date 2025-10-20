#!/usr/bin/env python3
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# Carrega o JSON como uma lista de dicionários
with open('bdados_venda.json', 'r') as f:
    json_data = f.read()
# --- Funções de Análise e Visualização ---

def carregar_dados_e_converter_dataframe(json_str):
    """Carrega o JSON e o converte para um DataFrame do Pandas,
    garantindo que a coluna de data esteja no formato correto."""
    
    # 1. Carregar JSON
    vendas = json.loads(json_str)
    
    # 2. Criar DataFrame
    df = pd.DataFrame(vendas)
    
    # 3. Converter a coluna 'data' para o tipo datetime (Essencial para análise temporal)
    df['data'] = pd.to_datetime(df['data'])
    
    return df

def agrupar_e_plotar_vendas_diarias(df):
    """Agrupa as vendas por dia, gera um gráfico de linha e o salva."""
    
    # Agrupamento: Soma o 'valor_total' para cada 'data'
    vendas_diarias = df.groupby('data')['valor_total'].sum()

    # Criação da pasta 'images' (Se ela não existir)
    pasta_imagens = 'images'
    os.makedirs(pasta_imagens, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_imagens, 'vendas_diarias.png')
    
    # --- Plotagem com Matplotlib ---
    plt.figure(figsize=(12, 6))
    vendas_diarias.plot(
        kind='line', 
        marker='o', 
        color='#007BFF', # Azul profissional
        linestyle='-',
        linewidth=2
    )
    
    # Configurações do Gráfico
    plt.title('Vendas Diárias do Mês de Outubro', fontsize=16, fontweight='bold')
    plt.xlabel('Dia do Mês', fontsize=12)
    plt.ylabel('Total Vendido (R$)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7) # Grid apenas no eixo Y
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Garante que todos os elementos caibam na imagem
    
    # Salvar o gráfico
    plt.savefig(caminho_arquivo)
    plt.close() # Fecha a figura para liberar memória

    print(f"\n[SUCESSO] Gráfico de Vendas Diárias salvo em: {caminho_arquivo}")
    
    return vendas_diarias


# --- Execução Principal ---

# 1. Carregar e preparar os dados
# (Substitua json_data pela leitura do arquivo real, se estiver rodando localmente)
df_vendas = carregar_dados_e_converter_dataframe(json_data)
print("DataFrame de Vendas carregado e pronto para análise.")
print(f"Total de vendas no DataFrame: {len(df_vendas)}")

# 2. Análise e Geração de Gráfico
vendas_por_dia = agrupar_e_plotar_vendas_diarias(df_vendas)

# 3. Exibir os resultados-chave da análise
print("\n--- Resultados Chave ---")
print(f"Média Diária de Vendas: R$ {vendas_por_dia.mean():.2f}")
print(f"Venda Máxima (Dia {vendas_por_dia.idxmax().strftime('%d/%m')}): R$ {vendas_por_dia.max():.2f}")

print("\n--- Top 5 Dias de Maior Venda ---")
# O .to_string() é usado para formatar a saída do Pandas de forma limpa no console
print(vendas_por_dia.sort_values(ascending=False).head(5).to_string())
