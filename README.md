# 📊 Dashboard de Vendas — Maxiline Fortaleza

Sistema de Dashboard Interativo para análise de vendas, desenvolvido com **Python**, **Streamlit**, **Plotly** e **Pandas**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Funcionalidades

- **Upload de Dados** — Excel (.xlsx) ou CSV
- **KPI Cards** — Total de Vendas, % Meta Global, Novos Clientes, Ticket Médio
- **Gráfico de Barras** — Realizado vs. Meta por Consultor
- **Gráfico de Tendência** — Vendas diárias, semanais ou mensais
- **Ranking de Consultores** — Ordenado por % de atingimento com medalhas 🥇🥈🥉
- **Comparativo Mensal** — Variação % entre meses
- **Filtros Interativos** — Por mês, período personalizado e consultor individual
- **Tema Dark/Light** — Toggle na sidebar
- **Paleta Profissional** — Azul marinho, cinza executivo e verde meta

## 📋 Colunas Esperadas no Arquivo

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| Data | Data | 2026-03-01 |
| Nome do Consultor | Texto | Anderson |
| Meta | Número | 25000 |
| Valor Realizado | Número | 23500.50 |
| Quantidade Vendas | Inteiro | 12 |
| Clientes Novos/Reativação | Inteiro | 3 |

## 🚀 Como Rodar

### Pré-requisitos
- Python 3.10 ou superior

### Instalação

```bash
# Clone o repositório
git clone https://github.com/willvernen/dashboard-vendas-maxiline.git
cd dashboard-vendas-maxiline

# Instale as dependências
python -m pip install -r requirements.txt

# (Opcional) Gere dados de exemplo
python gerar_dados_exemplo.py

# Rode o dashboard
python -m streamlit run app.py
```

O dashboard abrirá automaticamente em **http://localhost:8501**.

## 🌐 Deploy no Streamlit Cloud

1. Faça push do projeto para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Selecione `app.py` como arquivo principal
5. Clique em **Deploy**

## ➕ Adicionar Novo Vendedor

**Nos dados:** Basta incluir o nome na coluna `Nome do Consultor` do arquivo Excel/CSV. O dashboard detecta automaticamente.

**Na lista fixa:** Edite `CONSULTORES_FIXOS` em `app.py`:
```python
CONSULTORES_FIXOS = [
    "Anderson", "André", "Cleiton", "Daniel",
    "Francis", "Rodrigues", "Zarlon", "Sônia (E-Comerce)",
    "Novo Vendedor",  # ← adicione aqui
]
```

## 📁 Estrutura do Projeto

```
├── app.py                    # Dashboard principal
├── gerar_dados_exemplo.py    # Gerador de dados fictícios
├── dados_exemplo.xlsx        # Dados de exemplo (Fev + Mar 2026)
├── requirements.txt          # Dependências Python
├── .gitignore
└── README.md
```

## 🛠️ Stack

| Tecnologia | Uso |
|------------|-----|
| **Streamlit** | Framework web interativo |
| **Plotly** | Gráficos interativos |
| **Pandas** | Processamento de dados |
| **OpenPyXL** | Leitura de arquivos Excel |

---

Desenvolvido para **Maxiline Fortaleza** 🇧🇷
