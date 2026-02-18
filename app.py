import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Cacao Pulse 360", page_icon="🍫")

# Inyección de CSS para Título Gigante de 150px
st.markdown("""
    <style>
    .titulo-gigante {
        color: #800000;
        font-size: 150px; /* Tamaño extremo solicitado */
        font-weight: 900;
        text-align: center;
        line-height: 1; /* Ajusta el interlineado para que no ocupe demasiado espacio vertical */
        margin-top: -50px;
        margin-bottom: 10px;
        font-family: 'Arial Black', Gadget, sans-serif;
        letter-spacing: -5px; /* Estrecha un poco las letras para un look más moderno y compacto */
    }
    .subtitulo-central {
        text-align: center;
        color: #555555;
        margin-top: -10px;
        margin-bottom: 30px;
        font-size: 22px;
        font-weight: bold;
    }
    /* Estilo para los subencabezados de las secciones */
    .stSubheader {
        color: #800000 !format;
    }
    </style>
    """, unsafe_allow_html=True)

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
# El logo lo ponemos pequeño arriba a la izquierda para no distraer del título gigante
col_logo, _ = st.columns([1, 8])
with col_logo:
    nombre_logo = "logo_corona_bp.png"
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=120)

# Renderizado del Título de 150px
st.markdown('<p class="titulo-gigante">CACAO PULSE 360</p>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitulo-central">INTELIGENCIA DE MERCADO GLOBAL | REPORTE 2026</p>', unsafe_allow_html=True)

st.divider()

# 3. KPIs GLOBALES
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Stocks Globales (USDA)", "1.35M TM", "-4.2%")
with k2: st.metric("Consumo Mundial", "4.85M TM", "+1.8%")
with k3: st.metric("Exportaciones Globales", "4.20M TM", "-2.1%")
with k4: st.metric("Importación UE", "1.10M TM", "+0.5%")

st.divider()

# 4. MERCADOS: HISTÓRICO Y FUTUROS
col_hist, col_fut = st.columns(2)

with col_hist:
    titulo_con_icono("Futuros Cacao.PNG", "Histórico de Precios (USD/MT)")
    hist_data = {
        'Fecha': pd.date_range(start='2025-01-01', periods=12, freq='ME'),
        'Precio USD/MT': [8200, 8500, 9100, 9800, 9400, 9200, 9600, 9900, 10200, 9800, 9500, 9350]
    }
    df_hist = pd.DataFrame(hist_data)
    fig_hist = px.line(df_hist, x='Fecha', y='Precio USD/MT', markers=True)
    fig_hist.update_traces(line_color='#d35400', line_width=3)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_fut:
    titulo_con_icono("Futuros Cacao.PNG", "Mercado de Futuros (USD/MT)")
    vencimientos = {
        'Mes Vencimiento': ['Mar 26', 'May 26', 'Jul 26', 'Sep 26', 'Dic 26', 'Mar 27'],
        'Precio Proyectado': [9450, 9300, 9150, 8900, 8750, 8500]
    }
    df_venc = pd.DataFrame(vencimientos)
    fig_venc = px.line(df_venc, x='Mes Vencimiento', y='Precio Proyectado', markers=True, text='Precio Proyectado')
    fig_venc.update_traces(line=dict(color='#7e3412', width=4), marker=dict(size=12, color='#d35400'), textposition="top center")
    st.plotly_chart(fig_venc, use_container_width=True)

st.divider()

# 5. PRODUCCIÓN (GLOBO) Y STOCKS
col_prod, col_stock_p = st.columns([2, 1])

df_productores = pd.DataFrame({
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
    'Stocks_MT': [450000, 180000, 120000, 65000, 55000, 40000, 35000]
})

with col_prod:
    st.subheader("📍 Países donde se concentra la producción")
    fig_map = px.choropleth(df_productores, locations="ISO", color="Producción", color_continuous_scale="Oranges", projection="orthographic")
    fig_map.update_geos(projection_rotation=dict(lon=0, lat=10, roll=0), showocean=True, oceancolor="#e8f4f8")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550)
    st.plotly_chart(fig_map, use_container_width=True)

with col_stock_p:
    st.subheader("📦 Stocks en Origen (MT)")
    fig_stock_p = px.bar(df_productores.sort_values('Stocks_MT'), x='Stocks_MT', y='País', orientation='h', color='Stocks_MT', color_continuous_scale='Reds', text_auto='.2s')
    fig_stock_p.update_layout(showlegend=False, height=550)
    st.plotly_chart(fig_stock_p, use_container_width=True)

st.divider()

# 6. CONSUMO E IMPORTACIÓN
col_cons, col_imp = st.columns(2)

with col_cons:
    st.subheader("☕ Principales Países Consumidores (MT)")
    df_consumo = pd.DataFrame({
        'País': ['EE.UU.', 'Alemania', 'Francia', 'Reino Unido', 'Bélgica', 'Suiza', 'España'],
        'Consumo_MT': [795000, 380000, 245000, 210000, 185000, 110000, 88000]
    }).sort_values('Consumo_MT', ascending=True)
    fig_cons = px.bar(df_consumo, x='Consumo_MT', y='País', orientation='h', color='Consumo_MT', color_continuous_scale='YlOrBr', text_auto='.2s')
    st.plotly_chart(fig_cons, use_container_width=True)

with col_imp:
    titulo_con_icono("Principales Importadores.PNG", "Principales Importadores Globales (MT)")
    df_imp = pd.DataFrame({
        'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Bélgica', 'Malasia', 'España'],
        'TM': [750000, 680000, 520000, 310000, 290000, 85000]
    }).sort_values('TM', ascending=True)
    fig_imp = px.bar(df_imp, x='TM', y='País', orientation='h', color='TM', color_continuous_scale='Oranges', text_auto='.2s')
    st.plotly_chart(fig_imp, use_container_width=True)
