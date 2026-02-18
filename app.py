import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

# Configuración de la página
st.set_page_config(layout="wide", page_title="Cacao Decision Dashboard")

st.title("🍫 Cuadro de Mando: Mercado del Cacao 2026")
st.caption("Actualizado al 13/01/2026 basado en reportes ICCO y Yahoo Finance")

# --- COLUMNAS PRINCIPALES (Como en tu PDF) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Producción por País (TM)")
    # Datos extraídos de tu informe 
    data_prod = {
        'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún'],
        '2025': [2100000, 800000, 650000, 300000, 280000]
    }
    df_prod = pd.DataFrame(data_prod)
    fig_prod = go.Figure(data=[go.Bar(x=df_prod['País'], y=df_prod['2025'], marker_color='#d35400')])
    st.plotly_chart(fig_prod, use_container_width=True)

with col2:
    st.subheader("Evolución de Precios en Tiempo Real")
    # Conexión automática a mercado financiero
    ticker = "CC=F" 
    data_price = yf.download(ticker, period="1y")
    fig_price = go.Figure(data=[go.Scatter(x=data_price.index, y=data_price['Close'], line=dict(color='#d35400'))])
    st.plotly_chart(fig_price, use_container_width=True)

# --- SECCIÓN DE RIESGOS Y CLIMA ---
st.divider()
st.subheader("⚠️ Riesgos y Previsiones 2026")
c1, c2, c3 = st.columns(3)

with c1:
    st.info("**Clima:** Se espera que el cambio climático afecte negativamente la producción en África Occidental[cite: 37].")
with c2:
    st.warning("**Regulación:** La normativa EUDR (diciembre 2025) impactará los costes de trazabilidad[cite: 119].")
with c3:
    st.error("**Sanidad:** La enfermedad del brote hinchado amenaza la producción actual[cite: 118].")
