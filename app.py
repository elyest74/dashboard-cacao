import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Estratégico Cacao")

# Función auxiliar para mostrar Título con Icono
def titulo_con_icono(ruta_icono, texto_titulo):
    if os.path.exists(ruta_icono):
        c1, c2 = st.columns([0.1, 0.9])
        with c1:
            st.image(ruta_icono, width=40)
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
    st.title("SISTEMA DE MONITOREO: MERCADO DEL CACAO")
    st.caption("Fuentes: USDA, ICCO y Yahoo Finance | Datos actualizados 2026")

st.divider()

# 3. MÉTRICAS (KPIs)
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

with col_map:
    st.subheader("📍 Producción Mundial por País (TM)")
    df_paises = pd.DataFrame({
        'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
        'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
        'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
        'Exportación': [1650000, 620000, 410000, 210000, 190000, 10000, 145000]
    })
    fig_map = px.choropleth(df_paises, locations="ISO", color="Producción", color_continuous_scale="Oranges")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=350)
    st.plotly_chart(fig_map, use_container_width=True)

with col_bar:
    # ICONO: Exportaciones.PNG
    titulo_con_icono("Exportaciones.PNG", "Exportaciones (TM)")
    fig_exp = px.bar(df_paises.sort_values('Exportación'), x='Exportación', y='País', 
                     orientation='h', color_discrete_sequence=['#7e3412'])
    st.plotly_chart(fig_exp, use_container_width=True)

# 5. FINANZAS Y MERCADOS
st.divider()
col_fx, col_cocoa = st.columns(2)

with col_fx:
    # ICONO: Cambio USD EUR.PNG
    titulo_con_icono("Cambio USD EUR.PNG", "Tasa de Cambio EUR/USD")
    try:
        df_fx = yf.download("EURUSD=X", period="1y", interval="1d", progress=False)
        fig_fx = px.line(df_fx, y="Close")
        fig_fx.update_traces(line_color='#2E86C1')
        st.plotly_chart(fig_fx, use_container_width=True)
    except:
        st.error("Error en divisas")

with col_cocoa:
    # ICONO: Futuros Cacao.PNG
    titulo_con_icono("Futuros Cacao.PNG", "Precio Futuros Cacao")
    try:
        df_cc = yf.download("CC=F", period="1y", interval="1d", progress=False)
        fig_cc = px.area(df_cc, y="Close")
        fig_cc.update_traces(line_color='#d35400', fillcolor='rgba(211, 84, 0, 0.2)')
        st.plotly_chart(fig_cc, use_container_width=True)
    except:
        st.warning("Mercado no disponible")

# 6. IMPORTADORES
st.divider()
# ICONO: Principales Importadores.PNG
titulo_con_icono("Principales Importadores.PNG", "Principales Importadores Globales (TM)")

df_imp = pd.DataFrame({
    'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia', 'España'],
    'TM': [750000, 680000, 520000, 310000, 290000, 85000]
}).sort_values('TM', ascending=True)

fig_imp = px.bar(df_imp, x='TM', y='País', orientation='h', 
                 color='TM', color_continuous_scale='Oranges', text_auto='.2s')
fig_imp.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_imp, use_container_width=True)
