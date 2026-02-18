import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Cacao Corona 2026")

def titulo_con_icono(ruta_icono, texto_titulo):
    if os.path.exists(ruta_icono):
        c1, c2 = st.columns([0.07, 0.93])
        with c1:
            st.image(ruta_icono, width=45)
        with c2:
            st.subheader(texto_titulo)
    else:
        st.subheader(texto_titulo)

# 2. ENCABEZADO
col_logo, col_titulo = st.columns([1, 4])
nombre_logo = "logo_corona_bp.png"

with col_logo:
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        st.warning("⚠️ Logo no detectado")

with col_titulo:
    st.title("ESTRATEGIA GLOBAL DE COMPRAS: CACAO")
    st.caption(f"Referencia: ICE London / NY | Monitoreo de Mercado 2026")

st.divider()

# 3. KPIs USDA
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Stocks Globales (USDA)", "1.35M TM", "-4.2%")
with k2: st.metric("Consumo Mundial", "4.85M TM", "+1.8%")
with k3: st.metric("Exportaciones Globales", "4.20M TM", "-2.1%")
with k4: st.metric("Importación UE", "1.10M TM", "+0.5%")

st.divider()

# 4. MERCADOS: HISTÓRICO Y MERCADO DE FUTUROS
col_hist, col_fut = st.columns(2)

with col_hist:
    titulo_con_icono("Futuros Cacao.PNG", "Histórico de Precios (USD/MT)")
    hist_data = {
        'Fecha': pd.date_range(start='2025-01-01', periods=12, freq='ME'),
        'Precio USD/MT': [8200, 8500, 9100, 9800, 9400, 9200, 9600, 9900, 10200, 9800, 9500, 9350]
    }
    df_hist = pd.DataFrame(hist_data)
    fig_hist = px.line(df_hist, x='Fecha', y='Precio USD/MT', markers=True)
    fig_hist.update_traces(line_color='#d35400')
    fig_hist.update_layout(xaxis_title="Evolución Mensual", yaxis_title="Precio (USD/MT)")
    st.plotly_chart(fig_hist, use_container_width=True)

with col_fut:
    titulo_con_icono("Futuros Cacao.PNG", "Mercado de Futuros (USD/MT)")
    vencimientos = {
        'Mes Vencimiento': ['Mar 26', 'May 26', 'Jul 26', 'Sep
