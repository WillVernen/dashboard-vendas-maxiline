"""
Script para gerar o arquivo dados_exemplo.xlsx com dados fictícios
para teste do dashboard de vendas da Maxiline Fortaleza.
Gera dados de Fevereiro e Março de 2026.
"""
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

consultores = [
    "Anderson", "André", "Cleiton", "Daniel",
    "Francis", "Rodrigues", "Zarlon", "Sônia (E-Comerce)"
]

registros = []

# ── Fevereiro 2026 (28 dias) ────────────────────────────────────────────────
inicio_fev = datetime(2026, 2, 1)
for dia in range(28):
    data = inicio_fev + timedelta(days=dia)
    if data.weekday() == 6:  # Pular domingos
        continue
    for consultor in consultores:
        meta = random.choice([15000, 20000, 25000, 30000])
        fator = random.uniform(0.50, 1.30)  # Fev com desempenho um pouco menor
        valor_realizado = round(meta * fator, 2)
        qtd_vendas = random.randint(2, 18)
        clientes_novos = random.randint(0, 4)
        registros.append({
            "Data": data.strftime("%Y-%m-%d"),
            "Nome do Consultor": consultor,
            "Meta": meta,
            "Valor Realizado": valor_realizado,
            "Quantidade Vendas": qtd_vendas,
            "Clientes Novos/Reativação": clientes_novos,
        })

# ── Março 2026 (31 dias) ────────────────────────────────────────────────────
inicio_mar = datetime(2026, 3, 1)
for dia in range(31):
    data = inicio_mar + timedelta(days=dia)
    if data.weekday() == 6:  # Pular domingos
        continue
    for consultor in consultores:
        meta = random.choice([15000, 20000, 25000, 30000])
        fator = random.uniform(0.55, 1.35)  # Mar um pouco melhor
        valor_realizado = round(meta * fator, 2)
        qtd_vendas = random.randint(3, 20)
        clientes_novos = random.randint(0, 5)
        registros.append({
            "Data": data.strftime("%Y-%m-%d"),
            "Nome do Consultor": consultor,
            "Meta": meta,
            "Valor Realizado": valor_realizado,
            "Quantidade Vendas": qtd_vendas,
            "Clientes Novos/Reativação": clientes_novos,
        })

df = pd.DataFrame(registros)
df.to_excel("dados_exemplo.xlsx", index=False)
print(f"Arquivo dados_exemplo.xlsx gerado com {len(df)} registros (Fev + Mar 2026).")
