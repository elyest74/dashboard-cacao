import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Integral Cacao 2026")

# 2. ENCABEZADO
col_logo, col_titulo = st.columns([1, 4])
nombre_logo = "logo_corona_bp.png"

with col_logo:
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        st.warning(f"⚠️ Logo no encontrado")

with col_titulo:
    st.title("ESTRATEGIA GLOBAL DE COMPRAS: CACAO")
    st.caption("Fuente de datos: USDA, ICCO, Yahoo Finance | Actualizado: 2026")

st.divider()

# 3. FILA 1: MÉTRICAS CLAVE (KPIs) - Datos USDA/ICCO
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Stocks Globales (USDA 25/26)", value="1.35M TM", delta="-4.2%", delta_color="inverse")
    st.caption("Inventarios finales estimados")
with kpi2:
    st.metric(label="Consumo Internacional", value="4.85M TM", delta="+1.8%")
    st.caption("Molienda y demanda global")
with kpi3:
    st.metric(label="Déficit de Campaña", value="340K TM", delta="Presión Alcista")

# 4. FILA 2: MAPA Y EXPORTACIONES
col_mapa, col_exp = st.columns([2, 1])

with col_mapa:
    st.subheader("📍 Producción y Origen (TM)")
    df_prod = pd.DataFrame({
        'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
        'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
        'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000]
    })
    fig_mapa = px.choropleth(df_prod, locations="ISO", color="Producción", hover_name="País",
                           color_continuous_scale="Oranges")
    fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=350)
    st.plotly_chart(fig_mapa, use_container_width=True)

with col_exp:
    st.subheader("🚢 Exportaciones")
    # Datos de exportación principales
    df_exp = pd.DataFrame({
        'País': ['C. Marfil', 'Ghana', 'Ecuador', 'Camerún'],
        'TM': [1650000, 620000, 380000, 210000]
    }).sort_values('TM')
    fig_exp = px.bar(df_exp, x='TM', y='País', orientation='h', color_discrete_sequence=['#7e3412'])
    st.plotly_chart(fig_exp, use_container_width=True)

# 5. FILA 3: IMPORTACIONES Y DIVISAS
col_imp, col_fx = st.columns(2)

with col_imp:
    st.subheader("📥 Principales Importadores (TM)")
    df_imp = pd.DataFrame({
        'Región': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia'],
        'Importación': [750000, 680000, 520000, 310000, 290000]
    })
    fig_imp = px.pie(df_imp, values='Importación', names='Región', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.Oranges_r)
    st.plotly_chart(fig_imp, use_container_width=True)

with col_fx:
    st.subheader("💱 Tasa de Cambio EUR/USD (12M)")
    try:
        fx_data = yf.download("EURUSD=X", period="1y", interval="1d", progress=False)
        if not fx_data.empty:
            fig_fx = px.line(fx_data, y="Close", labels={'Close': 'Precio', 'Date': 'Fecha'})
            fig_fx.update_traces(line_color='#2E86C1') # Azul para diferenciar de cacao
            st.plotly_chart(fig_fx, use_container_width=True)
    except:
        st.error("No se pudo cargar la tasa EUR/USD")

# 6. FILA 4: PRECIOS DEL CACAO
st.divider()
st.subheader("📈 Evolución Precio Cacao Futuros (CC=F)")
try:
    cacao_data = yf.download("CC=F", period="1y", interval="1d", progress=False)
    fig_cacao = px.area(cacao_data, y="Close", labels={'Close': 'USD/MT'})
    fig_cacao.update_traces(line_color='#d35400', fillcolor='rgba(211, 84, 0, 0.2)')
    st.plotly_chart(fig_cacao, use_container_width=True)
except:
    st.error("Error al conectar con precios de cacao")
