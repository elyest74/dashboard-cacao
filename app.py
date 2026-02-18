import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Estratégico Cacao 2026")

# Función para Títulos con Iconos Personalizados
def titulo_con_icono(ruta_icono, texto_titulo):
    if os.path.exists(ruta_icono):
        c1, c2 = st.columns([0.07, 0.93])
        with c1:
            st.image(ruta_icono, width=45)
        with c2:
            st.subheader(texto_titulo)
    else:
        st.subheader(texto_titulo)
        st.caption(f"⚠️ Icono '{ruta_icono}' no encontrado en GitHub")

# 2. ENCABEZADO PRINCIPAL (LOGO CORONA)
col_logo, col_titulo = st.columns([1, 4])
nombre_logo = "logo_corona_bp.png"

with col_logo:
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        st.warning("⚠️ Logo Corona no detectado")

with col_titulo:
    st.title("SISTEMA DE MONITOREO: MERCADO DEL CACAO")
    st.caption("Fuentes: USDA, ICCO y Yahoo Finance | Datos actualizados 2026")

st.divider()

# 3. MÉTRICAS CLAVE (KPIs basados en datos USDA)
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

# 4. MAPA Y EXPORTACIONES (CON ICONO)
col_map, col_bar = st.columns([2, 1])

# Datos de Producción y Exportación
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
    titulo_con_icono("Exportaciones.PNG", "Exportaciones (TM)")
    fig_exp = px.bar(df_paises.sort_values('Exportación'), x='Exportación', y='País', 
                     orientation='h', color_discrete_sequence=['#7e3412'])
    fig_exp.update_layout(height=350, margin=dict(t=0, b=0))
    st.plotly_chart(fig_exp, use_container_width=True)

# 5. DATOS DE MERCADO CONECTADOS (EUR/USD y FUTUROS)
st.divider()
col_fx, col_cocoa = st.columns(2)

# Función de descarga reforzada
def extraer_mercado(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if not df.empty:
            df = df.reset_index()
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

with col_fx:
    titulo_con_icono("Cambio USD EUR.PNG", "Tasa de Cambio EUR/USD")
    data_fx = extraer_mercado("EURUSD=X")
    if not data_fx.empty:
        fig_fx = px.line(data_fx, x='Date', y='Close')
        fig_fx.update_traces(line_color='#2E86C1')
        st.plotly_chart(fig_fx, use_container_width=True)
    else:
        st.error("Conexión fallida con el servidor de divisas.")

with col_cocoa:
    titulo_con_icono("Futuros Cacao.PNG", "Precio Futuros Cacao")
    data_cc = extraer_mercado("CC=F")
    if not data_cc.empty:
        fig_cc = px.area(data_cc, x='Date', y='Close')
        fig_cc.update_traces(line_color='#d35400', fillcolor='rgba(211, 84, 0, 0.2)')
        st.plotly_chart(fig_cc, use_container_width=True)
    else:
        st.warning("⚠️ Los datos de Yahoo Finance no están disponibles ahora.")

# 6. IMPORTADORES (GRÁFICO DE BARRAS CON ICONO)
st.divider()
titulo_con_icono("Principales Importadores.PNG", "Principales Importadores Globales (TM)")

df_imp = pd.DataFrame({
    'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia', 'España'],
    'TM': [750000, 680000, 520000, 310000, 290000, 85000]
}).sort_values('TM', ascending=True)

fig_imp = px.bar(df_imp, x='TM', y='País', orientation='h', 
                 color='TM', color_continuous_scale='Oranges', text_auto='.2s')
fig_imp.update_layout(showlegend=False, height=400, margin=dict(t=20))
st.plotly_chart(fig_imp, use_container_width=True)
