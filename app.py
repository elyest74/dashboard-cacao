import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Estratégico Cacao")

# 2. ENCABEZADO PROFESIONAL
col_logo, col_titulo = st.columns([1, 4])
nombre_logo = "logo_corona_bp.png"

with col_logo:
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        st.warning("⚠️ Logo no detectado")

with col_titulo:
    st.title("SISTEMA DE MONITOREO: MERCADO DEL CACAO")
    st.caption("Fuentes: USDA, ICCO y Yahoo Finance | Datos actualizados 2026")

st.divider()

# 3. FILA DE MÉTRICAS (USDA / STOCKS / CONSUMO)
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

# 4. MAPA Y DATOS DE PAÍSES
col_map, col_bar = st.columns([2, 1])

df_paises = pd.DataFrame({
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
    'Exportación': [1650000, 620000, 410000, 210000, 190000, 10000, 145000]
})

with col_map:
    st.subheader("📍 Producción Mundial por País (TM)")
    fig_map = px.choropleth(df_paises, locations="ISO", color="Producción", 
                           hover_name="País", color_continuous_scale="Oranges")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=350)
    st.plotly_chart(fig_map, use_container_width=True)

with col_bar:
    st.subheader("🚢 Exportaciones (TM)")
    fig_exp = px.bar(df_paises.sort_values('Exportación'), x='Exportación', y='País', 
                     orientation='h', color_discrete_sequence=['#7e3412'])
    st.plotly_chart(fig_exp, use_container_width=True)

# 5. CONEXIÓN A MERCADOS (ESTE ES EL BLOQUE QUE ESTABA FALLANDO)
st.divider()
col_fx, col_cocoa = st.columns(2)

def obtener_datos(ticker):
    try:
        # Intentamos descargar con parámetros de seguridad
        data = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        return data
    except:
        return pd.DataFrame()

with col_fx:
    st.subheader("💱 Tasa de Cambio EUR/USD")
    df_fx = obtener_datos("EURUSD=X")
    if not df_fx.empty:
        fig_fx = px.line(df_fx, y="Close")
        fig_fx.update_traces(line_color='#2E86C1')
        st.plotly_chart(fig_fx, use_container_width=True)
    else:
        st.error("Servidor de divisas ocupado. Reintente en un momento.")

with col_cocoa:
    st.subheader("📈 Precio Futuros Cacao (CC=F)")
    df_cocoa = obtener_datos("CC=F")
    if not df_cocoa.empty:
        fig_cc = px.area(df_cocoa, y="Close")
        fig_cc.update_traces(line_color='#d35400', fillcolor='rgba(211, 84, 0, 0.2)')
        st.plotly_chart(fig_cc, use_container_width=True)
    else:
        # PLAN B: Si falla el mercado real, mostramos aviso informativo
        st.warning("⚠️ El mercado financiero está cerrado o la conexión falló. Intente refrescar la página.")

# 6. TABLA DE IMPORTADORES (USDA)
st.divider()
st.subheader("📥 Principales Importadores Globales")
df_imp = pd.DataFrame({
    'País Importador': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia', 'España'],
    'TM Importadas': [750000, 680000, 520000, 310000, 290000, 85000]
})
st.table(df_imp)
