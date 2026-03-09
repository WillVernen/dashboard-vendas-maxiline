"""
Dashboard Interativo de Vendas — Maxiline Fortaleza
Desenvolvido com Streamlit + Plotly + Pandas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Maxiline Fortaleza — Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# LISTA FIXA DE CONSULTORES
# ══════════════════════════════════════════════════════════════════════════════
CONSULTORES_FIXOS = [
    "Anderson", "André", "Cleiton", "Daniel",
    "Francis", "Rodrigues", "Zarlon", "Sônia (E-Comerce)",
]

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE CORES PROFISSIONAL
# ══════════════════════════════════════════════════════════════════════════════
AZUL_MARINHO = "#1B2A4A"
AZUL_MEDIO = "#2C4A7C"
CINZA_EXECUTIVO = "#4A5568"
CINZA_CLARO = "#A0AEC0"
VERDE_META = "#38A169"
VERDE_CLARO = "#68D391"
AMARELO = "#ECC94B"
VERMELHO = "#E53E3E"
BRANCO = "#FFFFFF"
FUNDO_DARK = "#0E1117"
FUNDO_CARD_DARK = "#1E2736"
FUNDO_LIGHT = "#F7FAFC"
FUNDO_CARD_LIGHT = "#FFFFFF"

# ══════════════════════════════════════════════════════════════════════════════
# CSS CUSTOMIZADO
# ══════════════════════════════════════════════════════════════════════════════

def aplicar_tema(dark_mode: bool):
    if dark_mode:
        bg = FUNDO_DARK
        card_bg = FUNDO_CARD_DARK
        text_color = "#E2E8F0"
        border_color = "#2D3748"
        subtitle_color = CINZA_CLARO
    else:
        bg = FUNDO_LIGHT
        card_bg = FUNDO_CARD_LIGHT
        text_color = "#1A202C"
        border_color = "#E2E8F0"
        subtitle_color = CINZA_EXECUTIVO

    st.markdown(f"""
    <style>
        /* ── Reset & base ───────────────────────────────────────── */
        .stApp {{
            background-color: {bg};
            color: {text_color};
        }}

        /* ── KPI Cards ──────────────────────────────────────────── */
        .kpi-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 28px 24px;
            text-align: center;
            box-shadow: 0 4px 24px rgba(0,0,0,0.12);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }}
        .kpi-title {{
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: {subtitle_color};
            margin-bottom: 8px;
        }}
        .kpi-value {{
            font-size: 2.2rem;
            font-weight: 800;
            color: {text_color};
            line-height: 1.1;
        }}
        .kpi-sub {{
            font-size: 0.8rem;
            color: {subtitle_color};
            margin-top: 6px;
        }}

        /* ── Header ─────────────────────────────────────────────── */
        .header-container {{
            background: linear-gradient(135deg, {AZUL_MARINHO} 0%, {AZUL_MEDIO} 100%);
            border-radius: 16px;
            padding: 32px 40px;
            margin-bottom: 32px;
            color: {BRANCO};
            box-shadow: 0 4px 24px rgba(27,42,74,0.3);
        }}
        .header-title {{
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
        }}
        .header-sub {{
            font-size: 1rem;
            opacity: 0.85;
            margin: 0;
        }}

        /* ── Section titles ─────────────────────────────────────── */
        .section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {text_color};
            margin: 32px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 3px solid {AZUL_MEDIO};
            display: inline-block;
        }}

        /* ── Ranking table ──────────────────────────────────────── */
        .ranking-row {{
            display: flex;
            align-items: center;
            padding: 14px 20px;
            border-radius: 12px;
            margin-bottom: 8px;
            background: {card_bg};
            border: 1px solid {border_color};
            transition: transform 0.15s ease;
        }}
        .ranking-row:hover {{
            transform: translateX(4px);
        }}
        .ranking-pos {{
            font-size: 1.3rem;
            font-weight: 800;
            min-width: 40px;
            color: {AZUL_MEDIO};
        }}
        .ranking-name {{
            flex: 1;
            font-weight: 600;
            font-size: 1rem;
            color: {text_color};
        }}
        .ranking-pct {{
            font-size: 1.1rem;
            font-weight: 700;
            padding: 4px 14px;
            border-radius: 20px;
        }}
        .pct-green {{ background: {VERDE_META}22; color: {VERDE_META}; }}
        .pct-yellow {{ background: {AMARELO}22; color: {AMARELO}; }}
        .pct-red {{ background: {VERMELHO}22; color: {VERMELHO}; }}

        /* ── Sidebar ────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background: {card_bg};
            border-right: 1px solid {border_color};
        }}
        section[data-testid="stSidebar"] .stMarkdown p {{
            color: {text_color};
        }}

        /* ── Plotly chart containers ────────────────────────────── */
        .chart-container {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}

        /* ── Comparativo mensal cards ───────────────────────────── */
        .comparativo-up {{ color: {VERDE_META}; font-weight: 700; }}
        .comparativo-down {{ color: {VERMELHO}; font-weight: 700; }}

        /* ── Hide streamlit footer & hamburger ──────────────────── */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

def carregar_dados(uploaded_file) -> pd.DataFrame | None:
    """Carrega e valida o arquivo enviado pelo usuário."""
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        colunas_necessarias = [
            "Data", "Nome do Consultor", "Meta",
            "Valor Realizado", "Quantidade Vendas",
            "Clientes Novos/Reativação",
        ]
        faltando = [c for c in colunas_necessarias if c not in df.columns]
        if faltando:
            st.error(f"⚠️ Colunas ausentes no arquivo: **{', '.join(faltando)}**")
            return None

        df["Data"] = pd.to_datetime(df["Data"], dayfirst=False)
        df["Meta"] = pd.to_numeric(df["Meta"], errors="coerce").fillna(0)
        df["Valor Realizado"] = pd.to_numeric(df["Valor Realizado"], errors="coerce").fillna(0)
        df["Quantidade Vendas"] = pd.to_numeric(df["Quantidade Vendas"], errors="coerce").fillna(0)
        df["Clientes Novos/Reativação"] = pd.to_numeric(df["Clientes Novos/Reativação"], errors="coerce").fillna(0)

        # Cálculos automáticos
        df["% Atingimento"] = df.apply(
            lambda r: round((r["Valor Realizado"] / r["Meta"]) * 100, 1) if r["Meta"] > 0 else 0, axis=1
        )
        df["Ticket Médio"] = df.apply(
            lambda r: round(r["Valor Realizado"] / r["Quantidade Vendas"], 2) if r["Quantidade Vendas"] > 0 else 0, axis=1
        )
        return df

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
        return None


def formatar_brl(valor: float) -> str:
    """Formata valor em Real brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def kpi_card(titulo: str, valor: str, subtitulo: str = "", cor_destaque: str = AZUL_MEDIO):
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{titulo}</div>
        <div class="kpi-value" style="color: {cor_destaque};">{valor}</div>
        <div class="kpi-sub">{subtitulo}</div>
    </div>
    """


MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
    st.markdown("### 📊 Maxiline Dashboard")
    st.markdown("---")

    dark_mode = st.toggle("🌙 Modo Escuro", value=True)
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📁 Carregar Dados (Excel ou CSV)",
        type=["xlsx", "xls", "csv"],
        help="Envie um arquivo com as colunas: Data, Nome do Consultor, Meta, Valor Realizado, Quantidade Vendas, Clientes Novos/Reativação",
    )

# Aplicar tema
aplicar_tema(dark_mode)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="header-container">
    <p class="header-title">📊 Dashboard de Vendas</p>
    <p class="header-sub">Maxiline Fortaleza — Análise de Performance dos Consultores</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROCESSAMENTO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px;">
        <p style="font-size: 3rem; margin-bottom: 8px;">📂</p>
        <p style="font-size: 1.2rem; font-weight: 600; opacity: 0.7;">
            Envie um arquivo Excel ou CSV na barra lateral para começar.
        </p>
        <p style="font-size: 0.9rem; opacity: 0.5;">
            Colunas esperadas: Data · Nome do Consultor · Meta · Valor Realizado · Quantidade Vendas · Clientes Novos/Reativação
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df_original = carregar_dados(uploaded_file)
if df_original is None:
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# FILTROS NA SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔎 Filtros")

    # ── Filtro por Mês ──────────────────────────────────────────────────────
    meses_disponiveis = sorted(df_original["Data"].dt.to_period("M").unique())
    opcoes_meses = ["Todos os Meses"] + [
        f"{MESES_PT.get(m.month, m.month)} {m.year}" for m in meses_disponiveis
    ]
    filtro_mes = st.selectbox("📆 Mês", options=opcoes_meses, index=0)

    # ── Filtro por Período (Data) ───────────────────────────────────────────
    data_min = df_original["Data"].min().date()
    data_max = df_original["Data"].max().date()
    filtro_datas = st.date_input(
        "📅 Período Personalizado",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max,
    )

    st.markdown("---")

    # ── Filtro por Consultor ────────────────────────────────────────────────
    consultores_nos_dados = list(df_original["Nome do Consultor"].unique())
    consultores_disponiveis = [c for c in CONSULTORES_FIXOS if c in consultores_nos_dados]
    outros = [c for c in consultores_nos_dados if c not in CONSULTORES_FIXOS]
    todos_consultores = consultores_disponiveis + sorted(outros)

    st.markdown("**👤 Consultores**")

    # Botões rápidos
    col_sel, col_limp = st.columns(2)
    with col_sel:
        selecionar_todos = st.button("✅ Todos", use_container_width=True)
    with col_limp:
        limpar_selecao = st.button("❌ Limpar", use_container_width=True)

    # Definir default baseado nos botões
    if selecionar_todos:
        default_consultores = todos_consultores
    elif limpar_selecao:
        default_consultores = []
    else:
        default_consultores = todos_consultores

    filtro_consultores = st.multiselect(
        "Selecione os consultores",
        options=todos_consultores,
        default=default_consultores,
        label_visibility="collapsed",
    )

    # ── Como adicionar novo vendedor ────────────────────────────────────────
    st.markdown("---")
    with st.expander("➕ Adicionar Novo Vendedor"):
        st.markdown("""
        **Passo a passo:**

        1. Abra o arquivo **Excel/CSV** de dados
        2. Adicione novas linhas com o nome do novo vendedor na coluna **"Nome do Consultor"**
        3. Preencha todas as colunas obrigatórias
        4. Salve e faça **upload** novamente

        O dashboard detecta automaticamente qualquer novo consultor presente nos dados!

        **Para adicionar na lista fixa**, edite a variável `CONSULTORES_FIXOS` no arquivo `app.py`:
        ```python
        CONSULTORES_FIXOS = [
            "Anderson", "André", ...
            "Novo Vendedor",  # Adicione aqui
        ]
        ```
        """)

# ══════════════════════════════════════════════════════════════════════════════
# APLICAR FILTROS
# ══════════════════════════════════════════════════════════════════════════════
df = df_original.copy()

# Filtro de mês
if filtro_mes != "Todos os Meses":
    # Extrair mês/ano da seleção
    idx_mes = opcoes_meses.index(filtro_mes) - 1  # -1 por causa do "Todos"
    periodo_selecionado = meses_disponiveis[idx_mes]
    df = df[df["Data"].dt.to_period("M") == periodo_selecionado]

# Filtro de período personalizado
if isinstance(filtro_datas, tuple) and len(filtro_datas) == 2:
    df = df[(df["Data"].dt.date >= filtro_datas[0]) & (df["Data"].dt.date <= filtro_datas[1])]

# Filtro de consultores
df = df[df["Nome do Consultor"].isin(filtro_consultores)]

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# Info do filtro ativo
periodo_info = filtro_mes if filtro_mes != "Todos os Meses" else "Todo o Período"
n_consultores = len(filtro_consultores)
st.caption(f"📌 Exibindo: **{periodo_info}** · **{n_consultores}** consultor(es) · **{len(df)}** registros")

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
total_vendas = df["Valor Realizado"].sum()
total_meta = df["Meta"].sum()
pct_meta_global = round((total_vendas / total_meta) * 100, 1) if total_meta > 0 else 0
total_novos = int(df["Clientes Novos/Reativação"].sum())
ticket_medio_geral = round(total_vendas / df["Quantidade Vendas"].sum(), 2) if df["Quantidade Vendas"].sum() > 0 else 0

cor_meta = VERDE_META if pct_meta_global >= 100 else (AMARELO if pct_meta_global >= 70 else VERMELHO)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(kpi_card(
        "Total Geral de Vendas",
        formatar_brl(total_vendas),
        f"{int(df['Quantidade Vendas'].sum())} vendas realizadas",
        AZUL_MEDIO,
    ), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_card(
        "% Meta Global",
        f"{pct_meta_global}%",
        f"Meta: {formatar_brl(total_meta)}",
        cor_meta,
    ), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_card(
        "Novos Clientes / Reativação",
        f"{total_novos}",
        "clientes no período",
        VERDE_META,
    ), unsafe_allow_html=True)
with col4:
    st.markdown(kpi_card(
        "Ticket Médio Geral",
        formatar_brl(ticket_medio_geral),
        "por venda no período",
        AZUL_MEDIO,
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMPARATIVO MENSAL (se tiver mais de 1 mês)
# ══════════════════════════════════════════════════════════════════════════════
meses_no_filtro = df["Data"].dt.to_period("M").unique()
if len(meses_no_filtro) >= 2 and filtro_mes == "Todos os Meses":
    st.markdown('<div class="section-title">📅 Comparativo Mensal</div>', unsafe_allow_html=True)

    comparativo = df.groupby(df["Data"].dt.to_period("M")).agg(
        Vendas=("Valor Realizado", "sum"),
        Meta=("Meta", "sum"),
        Qtd_Vendas=("Quantidade Vendas", "sum"),
        Novos=("Clientes Novos/Reativação", "sum"),
    ).reset_index()
    comparativo["Mês"] = comparativo["Data"].apply(lambda p: f"{MESES_PT.get(p.month, p.month)} {p.year}")
    comparativo["% Meta"] = (comparativo["Vendas"] / comparativo["Meta"] * 100).round(1)

    cols_comp = st.columns(len(comparativo))
    for idx, (_, row) in enumerate(comparativo.iterrows()):
        with cols_comp[idx]:
            cor_m = VERDE_META if row["% Meta"] >= 100 else (AMARELO if row["% Meta"] >= 70 else VERMELHO)
            st.markdown(kpi_card(
                row["Mês"],
                formatar_brl(row["Vendas"]),
                f"Meta: {row['% Meta']}% · {int(row['Qtd_Vendas'])} vendas · {int(row['Novos'])} novos",
                cor_m,
            ), unsafe_allow_html=True)

    # Variação entre meses
    if len(comparativo) == 2:
        vendas_ant = comparativo.iloc[0]["Vendas"]
        vendas_atu = comparativo.iloc[1]["Vendas"]
        variacao = ((vendas_atu - vendas_ant) / vendas_ant * 100) if vendas_ant > 0 else 0
        seta = "↑" if variacao >= 0 else "↓"
        cor_var = "comparativo-up" if variacao >= 0 else "comparativo-down"
        st.markdown(
            f'<p style="text-align:center; margin-top:12px; font-size:1rem;">'
            f'Variação: <span class="{cor_var}">{seta} {abs(variacao):.1f}%</span> '
            f'de {comparativo.iloc[0]["Mês"]} para {comparativo.iloc[1]["Mês"]}'
            f'</p>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE BARRAS — Realizado vs Meta por Consultor
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Realizado vs. Meta por Consultor</div>', unsafe_allow_html=True)

resumo = df.groupby("Nome do Consultor").agg(
    Meta=("Meta", "sum"),
    Realizado=("Valor Realizado", "sum"),
).reset_index().sort_values("Realizado", ascending=True)

chart_bg = FUNDO_CARD_DARK if dark_mode else FUNDO_CARD_LIGHT
chart_text = "#E2E8F0" if dark_mode else "#1A202C"
chart_grid = "#2D3748" if dark_mode else "#E2E8F0"

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    y=resumo["Nome do Consultor"],
    x=resumo["Meta"],
    name="Meta",
    orientation="h",
    marker_color=CINZA_CLARO,
    marker_line_width=0,
    text=resumo["Meta"].apply(lambda v: formatar_brl(v)),
    textposition="inside",
    textfont=dict(size=11, color=BRANCO),
))
fig_bar.add_trace(go.Bar(
    y=resumo["Nome do Consultor"],
    x=resumo["Realizado"],
    name="Realizado",
    orientation="h",
    marker_color=[VERDE_META if r >= m else VERMELHO for r, m in zip(resumo["Realizado"], resumo["Meta"])],
    marker_line_width=0,
    text=resumo["Realizado"].apply(lambda v: formatar_brl(v)),
    textposition="inside",
    textfont=dict(size=11, color=BRANCO),
))

fig_bar.update_layout(
    barmode="group",
    height=max(320, len(resumo) * 55),
    margin=dict(l=0, r=20, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=chart_text, size=12),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        font=dict(size=12),
    ),
    xaxis=dict(showgrid=True, gridcolor=chart_grid, gridwidth=1, zeroline=False),
    yaxis=dict(showgrid=False),
)

st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE TENDÊNCIA — Vendas Diárias / Semanais
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Tendência de Vendas</div>', unsafe_allow_html=True)

col_agg, _ = st.columns([1, 3])
with col_agg:
    agregacao = st.radio("Agrupar por:", ["Diário", "Semanal", "Mensal"], horizontal=True)

vendas_tempo = df.copy()
if agregacao == "Semanal":
    vendas_tempo["Período"] = vendas_tempo["Data"].dt.to_period("W").apply(lambda p: p.start_time)
    vendas_agg = vendas_tempo.groupby("Período").agg(
        Vendas=("Valor Realizado", "sum"),
        Meta=("Meta", "sum"),
    ).reset_index()
    x_col = "Período"
elif agregacao == "Mensal":
    vendas_tempo["Período"] = vendas_tempo["Data"].dt.to_period("M").apply(lambda p: p.start_time)
    vendas_agg = vendas_tempo.groupby("Período").agg(
        Vendas=("Valor Realizado", "sum"),
        Meta=("Meta", "sum"),
    ).reset_index()
    x_col = "Período"
else:
    vendas_agg = vendas_tempo.groupby("Data").agg(
        Vendas=("Valor Realizado", "sum"),
        Meta=("Meta", "sum"),
    ).reset_index()
    x_col = "Data"

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=vendas_agg[x_col],
    y=vendas_agg["Meta"],
    name="Meta",
    mode="lines+markers",
    line=dict(color=CINZA_CLARO, width=2, dash="dash"),
    marker=dict(size=6),
))
fig_line.add_trace(go.Scatter(
    x=vendas_agg[x_col],
    y=vendas_agg["Vendas"],
    name="Vendas Realizadas",
    mode="lines+markers",
    line=dict(color=VERDE_META, width=3),
    marker=dict(size=7),
    fill="tozeroy",
    fillcolor=f"rgba(56,161,105,0.1)",
))

fig_line.update_layout(
    height=380,
    margin=dict(l=0, r=20, t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=chart_text, size=12),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        font=dict(size=12),
    ),
    xaxis=dict(showgrid=True, gridcolor=chart_grid, gridwidth=1),
    yaxis=dict(showgrid=True, gridcolor=chart_grid, gridwidth=1, zeroline=False),
    hovermode="x unified",
)

st.plotly_chart(fig_line, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# RANKING DE CONSULTORES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🏆 Ranking dos Consultores</div>', unsafe_allow_html=True)

ranking = df.groupby("Nome do Consultor").agg(
    Meta=("Meta", "sum"),
    Realizado=("Valor Realizado", "sum"),
    Vendas=("Quantidade Vendas", "sum"),
    Novos_Clientes=("Clientes Novos/Reativação", "sum"),
).reset_index()

ranking["% Atingimento"] = ranking.apply(
    lambda r: round((r["Realizado"] / r["Meta"]) * 100, 1) if r["Meta"] > 0 else 0, axis=1
)
ranking["Ticket Médio"] = ranking.apply(
    lambda r: round(r["Realizado"] / r["Vendas"], 2) if r["Vendas"] > 0 else 0, axis=1
)
ranking = ranking.sort_values("% Atingimento", ascending=False).reset_index(drop=True)

# Medalhas para top 3
medalhas = ["🥇", "🥈", "🥉"]

ranking_html = ""
for i, row in ranking.iterrows():
    pct = row["% Atingimento"]
    if pct >= 100:
        cor_class = "pct-green"
    elif pct >= 70:
        cor_class = "pct-yellow"
    else:
        cor_class = "pct-red"

    pos = medalhas[i] if i < 3 else f"{i+1}º"

    ranking_html += f"""
    <div class="ranking-row">
        <span class="ranking-pos">{pos}</span>
        <span class="ranking-name">{row['Nome do Consultor']}</span>
        <span style="flex:1; font-size:0.85rem; opacity:0.7;">
            {formatar_brl(row['Realizado'])} &nbsp;·&nbsp;
            {int(row['Vendas'])} vendas &nbsp;·&nbsp;
            Ticket: {formatar_brl(row['Ticket Médio'])} &nbsp;·&nbsp;
            {int(row['Novos_Clientes'])} novos
        </span>
        <span class="ranking-pct {cor_class}">{pct}%</span>
    </div>
    """

st.markdown(ranking_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABELA DETALHADA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📋 Ver tabela detalhada de dados"):
    display_df = df.copy()
    display_df["Data"] = display_df["Data"].dt.strftime("%d/%m/%Y")
    display_df["Meta"] = display_df["Meta"].apply(formatar_brl)
    display_df["Valor Realizado"] = display_df["Valor Realizado"].apply(formatar_brl)
    display_df["Ticket Médio"] = display_df["Ticket Médio"].apply(formatar_brl)
    display_df["% Atingimento"] = display_df["% Atingimento"].apply(lambda x: f"{x}%")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# RODAPÉ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    f"""<p style="text-align:center; font-size:0.8rem; opacity:0.5;">
    Maxiline Fortaleza — Dashboard de Vendas · {datetime.now().strftime('%Y')}
    </p>""",
    unsafe_allow_html=True,
)
