import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Cacao Corona 2026")

# Función para Títulos con Iconos
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
    st.caption(f"Referencia: Informe 13/01/2026 | Datos BCE/Mercados: {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# 3. MÉTRICAS (KPIs USDA)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Stocks Globales (USDA)", "1.35M TM", "-4.2%")
with k2:
    st.metric("Consumo Mundial", "4.85M TM", "+1.8%")
with k3:
    st.metric("Exportaciones Globales", "4.20M TM", "-2.1%")
with k4:
    st.metric("Importación UE", "1.10M TM", "+0.5%")

st.divider()

# 4. MAPA Y EXPORTACIONES
col_map, col_bar = st.columns([2, 1])

df_paises = pd.DataFrame({
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
    'Exportación': [1650000, 620000, 410000, 210000, 190000, 10000, 145000]
})

with col_map:
    st.subheader("📍 Producción Mundial por País (TM)")
    fig_map = px.choropleth(df_paises, locations="ISO", color="Producción", color_continuous_scale="Oranges")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=350)
    st.plotly_chart(fig_map, use_container_width=True)

with col_bar:
    titulo_con_icono("Exportaciones.PNG", "Exportaciones (TM)")
    df_exp_sorted = df_paises.sort_values('Exportación')
    fig_exp = px.
