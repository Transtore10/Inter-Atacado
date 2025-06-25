import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard Inter & Atacado")

# Estilo visual leve
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f4f6f9;
        }
        .section-title {
            font-size: 22px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 10px;
            color: #1d3557;
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }
    </style>
""", unsafe_allow_html=True)

abas = st.tabs(["📄 Capa", "📘 Sumário", "🌎 Pedidos Internacionais", "🏷️ Pedidos Atacados"])

with abas[0]:
    st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; height: 85vh;'>
        <div style='text-align: center;'>
            <div style='font-size: 56px; font-weight: bold; color: #1d3557;'>Dashboard Inter & Atacado</div>
            <div style='font-size: 20px; color: #457b9d; margin-top: 15px;'>Transtore 2025</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with abas[1]:
    st.markdown("<div class='section-title'>📘 Sumário</div>", unsafe_allow_html=True)
    st.write("- Evolução de pedidos por canal e país (Internacional)")
    st.write("- Evolução mensal de pedidos atacadistas")
    st.write("- Produtos mais vendidos no atacado")
    st.write("- Prazos médios por etapa (Internacional e Atacado)")
    st.write("- Principais problemas logísticos (Internacional)")
    st.write("- Situação de pagamentos internacionais (Wise)")

with abas[2]:
    st.markdown("<div class='section-title'>🌎 Pedidos Internacionais</div>", unsafe_allow_html=True)
    df_paises = pd.read_excel("planilha_dashboard_modelo.xlsx", sheet_name="Internacional_Paises")
    df_entradas = pd.read_excel("planilha_dashboard_modelo.xlsx", sheet_name="Internacional_Entradas")

    pais_filtro = st.selectbox("Filtrar por País:", options=["Todos"] + list(df_paises["País"].unique()))
    df_paises_plot = df_paises if pais_filtro == "Todos" else df_paises[df_paises["País"] == pais_filtro]
    fig_paises = px.bar(df_paises_plot, x="País", y="Pedidos", color="Pedidos", text="Pedidos", text_auto=True,
                        template="simple_white", color_continuous_scale="Blues")
    fig_paises.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig_paises, use_container_width=True)

    st.markdown("#### Evolução Mensal de Pedidos Internacionais")
    canal_opcao = st.selectbox("Filtrar por Canal:", options=["Todos"] + list(df_entradas.columns[1:]))
    df_plot = df_entradas.melt(id_vars="Mês", var_name="Canal", value_name="Pedidos")
    if canal_opcao != "Todos":
        df_plot = df_plot[df_plot["Canal"] == canal_opcao]

    df_plot["Pedidos"] = pd.to_numeric(df_plot["Pedidos"], errors="coerce")
    fig_entradas = px.line(df_plot, x="Mês", y="Pedidos", color="Canal", markers=True,
                           template="simple_white", color_discrete_sequence=px.colors.qualitative.Set2)

    for canal in df_plot["Canal"].unique():
        df_sub = df_plot[df_plot["Canal"] == canal]
        fig_entradas.add_scatter(
            x=df_sub["Mês"],
            y=df_sub["Pedidos"],
            mode="text",
            text=df_sub["Pedidos"].fillna(0).astype(int).astype(str),
            textposition="top center",
            showlegend=False
        )

    st.plotly_chart(fig_entradas, use_container_width=True)

with abas[3]:
    st.markdown("<div class='section-title'>🏷️ Pedidos Atacados</div>", unsafe_allow_html=True)
    df_mensal_atacado = pd.read_excel("planilha_dashboard_modelo.xlsx", sheet_name="Atacado_Mensal")
    df_top_atacado = pd.read_excel("planilha_dashboard_modelo.xlsx", sheet_name="Top_Produtos_Atacado")

    st.markdown("#### Evolução Mensal de Pedidos Atacados")
    df_mensal_atacado["Pedidos"] = pd.to_numeric(df_mensal_atacado["Pedidos"], errors="coerce")
    fig_atacado = px.line(df_mensal_atacado, x="Mês", y="Pedidos", markers=True,
                          template="simple_white", color_discrete_sequence=["#4a90e2"])
    fig_atacado.add_scatter(
        x=df_mensal_atacado["Mês"],
        y=df_mensal_atacado["Pedidos"],
        mode="text",
        text=df_mensal_atacado["Pedidos"].fillna(0).astype(int).astype(str),
        textposition="top center",
        showlegend=False
    )
    st.plotly_chart(fig_atacado, use_container_width=True)

    st.markdown("#### Produtos Mais Vendidos no Atacado")
    fig_top = px.bar(df_top_atacado, x="Produto", y="Quantidade", color="Quantidade", text="Quantidade",
                     template="simple_white", color_continuous_scale="Oranges")
    fig_top.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("#### Prazos Médios por Etapa Atacado")
    df_prazos_atacado = pd.DataFrame({
        "Etapa": ["Chegada Estoque → Saída Estoque", "Documentação → Despacho"],
        "Dias": [5, 1]
    })
    fig_prazos_atacado = px.bar(df_prazos_atacado, x="Dias", y="Etapa", orientation="h", text="Dias",
                                template="simple_white", color="Dias", color_continuous_scale="Teal")
    fig_prazos_atacado.update_traces(texttemplate='%{text} dias', textposition='outside')
    st.plotly_chart(fig_prazos_atacado, use_container_width=True)
