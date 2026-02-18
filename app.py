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
    fig_exp = px.bar(df_exp_sorted, x='Exportación', y='País', orientation='h', color_discrete_sequence=['#7e3412'])
    fig_exp.update_layout(height=350)
    st.plotly_chart(fig_exp, use_container_width=True)

# 5. CONEXIÓN REFORZADA A MERCADOS
st.divider()
col_fx, col_cocoa = st.columns(2)

@st.cache_data(ttl=3600) # Guarda los datos 1 hora para evitar bloqueos
def obtener_fx_bce():
    try:
        url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
        df = pd.read_csv(url, compression='zip')
        df_usd = df[['Date', 'USD']].copy()
        df_usd['Date'] = pd.to_datetime(df_usd['Date'])
        return df_usd.sort_values('Date').tail(180)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def descargar_datos_cacao():
    try:
        # Usamos Ticker para mayor estabilidad
        cacao = yf.Ticker("CC=F")
        df = cacao.history(period="1y")
        if not df.empty:
            df = df.reset_index()
            # Aplanamos MultiIndex si Yahoo lo envía
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

with col_fx:
    titulo_con_icono("Cambio USD EUR.PNG", "Tasa de Cambio EUR/USD (BCE)")
    df_fx = obtener_fx_bce()
    if not df_fx.empty:
        fig_fx = px.line(df_fx, x='Date', y='USD')
        fig_fx.update_traces(line_color='#2E86C1')
        st.plotly_chart(fig_fx, use_container_width=True)
    else:
        st.error("Error al conectar con el BCE.")

with col_cocoa:
    titulo_con_icono("Futuros Cacao.PNG", "Precio Cacao (ICE US Cocoa)")
    df_cc = descargar_datos_cacao()
    if not df_cc.empty:
        fig_cc = px.area(df_cc, x='Date', y='Close')
        fig_cc.update_traces(line_color='#d35400', fillcolor='rgba(211, 84, 0, 0.2)')
        st.plotly_chart(fig_cc, use_container_width=True)
    else:
        # MENSAJE DE SEGURIDAD SI TODO FALLA
        st.warning("⚠️ Servicio de datos saturado. Mostrando última referencia conocida: ~9,200 USD/MT")
        st.info("Sugerencia: Haz clic en el menú superior derecho de la app y selecciona 'Clear Cache' para reintentar.")

# 6. IMPORTADORES
st.divider()
titulo_con_icono("Principales Importadores.PNG", "Principales Importadores Globales (TM)")

df_imp = pd.DataFrame({
    'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia', 'España'],
    'TM': [750000, 680000, 520000, 310000, 290000, 85000]
}).sort_values('TM', ascending=True)

fig_imp = px.bar(df_imp, x='TM', y='País', orientation='h', color='TM', color_continuous_scale='Oranges', text_auto='.2s')
st.plotly_chart(fig_imp, use_container_width=True)
