import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Cacao Pulse 360", page_icon="🍫")

# Estilos CSS (Alineación, Títulos, y Pie de página)
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .main-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-container {
        max-width: 220px;
        height: auto;
    }
    .titulo-gigante {
        color: #800000;
        font-size: clamp(40px, 7vw, 90px);
        font-weight: 800;
        margin: 10px 0 0px 0;
        line-height: 1;
        letter-spacing: -2px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .subtitulo-inteligencia {
        color: #555555;
        font-size: 18px;
        font-weight: 500;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 5px;
    }
    .footer-autor {
        text-align: center;
        color: #800000;
        font-weight: bold;
        font-size: 20px;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #eeeeee;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO CENTRADO (LOGO + TÍTULO)
nombre_logo = "logo_corona_bp.png"
logo_html = ""
if os.path.exists(nombre_logo):
    with open(nombre_logo, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
        logo_html = f'<img src="data:image/png;base64,{data}" class="logo-container">'

st.markdown(f"""
    <div class="main-header">
        {logo_html}
        <h1 class="titulo-gigante">CACAO PULSE 360</h1>
        <p class="subtitulo-inteligencia">Inteligencia de Mercado Global | Reporte 2026</p>
    </div>
    """, unsafe_allow_html=True)

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
    st.subheader("📉 Histórico de Precios (USD/MT)")
    hist_data = {'Fecha': pd.date_range(start='2025-01-01', periods=12, freq='ME'),
                 'Precio USD/MT': [8200, 8500, 9100, 9800, 9400, 9200, 9600, 9900, 10200, 9800, 9500, 9350]}
    df_hist = pd.DataFrame(hist_data)
    fig_hist = px.line(df_hist, x='Fecha', y='Precio USD/MT', markers=True)
    fig_hist.update_traces(line_color='#d35400', line_width=3)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_fut:
    st.subheader("📅 Mercado de Futuros (USD/MT)")
    vencimientos = {'Mes': ['Mar 26', 'May 26', 'Jul 26', 'Sep 26', 'Dic 26', 'Mar 27'],
                    'Precio': [9450, 9300, 9150, 8900, 8750, 8500]}
    df_venc = pd.DataFrame(vencimientos)
    fig_venc = px.line(df_venc, x='Mes', y='Precio', markers=True, text='Precio')
    fig_venc.update_traces(line=dict(color='#7e3412', width=4), textposition="top center")
    st.plotly_chart(fig_venc, use_container_width=True)

st.divider()

# 5. PRODUCCIÓN (GLOBO), EXPORTACIÓN Y STOCKS
col_prod, col_stock_p = st.columns([2, 1])

df_productores = pd.DataFrame({
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
    'Exportación': [1650000, 620000, 410000, 210000, 190000, 10000, 145000],
    'Stocks_MT': [450000, 180000, 120000, 65000, 55000, 40000, 35000]
})

with col_prod:
    st.subheader("📍 Países donde se concentra la producción")
    fig_map = px.choropleth(df_productores, locations="ISO", color="Producción", color_continuous_scale="Oranges", projection="orthographic")
    fig_map.update_geos(projection_rotation=dict(lon=0, lat=10, roll=0), showocean=True, oceancolor="#e8f4f8")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

with col_stock_p:
    st.subheader("📦 Stocks en Origen (MT)")
    fig_stock_p = px.bar(df_productores.sort_values('Stocks_MT'), x='Stocks_MT', y='País', orientation='h', color='Stocks_MT', color_continuous_scale='Reds')
    fig_stock_p.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_stock_p, use_container_width=True)

st.divider()

# 6. EXPORTACIONES, CONSUMO E IMPORTADORES
col_exp, col_cons, col_imp = st.columns(3)

with col_exp:
    st.subheader("🚢 Exportaciones por País (MT)")
    fig_exp = px.bar(df_productores.sort_values('Exportación'), x='Exportación', y='País', orientation='h', color_discrete_sequence=['#d35400'])
    st.plotly_chart(fig_exp, use_container_width=True)

with col_cons:
    st.subheader("☕ Principales Consumidores (MT)")
    df_consumo = pd.DataFrame({'País': ['EE.UU.', 'Alemania', 'Francia', 'Reino Unido', 'España'],
                               'MT': [795000, 380000, 245000, 210000, 88000]})
    fig_cons = px.bar(df_consumo.sort_values('MT'), x='MT', y='País', orientation='h', color_discrete_sequence=['#a04000'])
    st.plotly_chart(fig_cons, use_container_width=True)

with col_imp:
    st.subheader("📥 Principales Importadores (MT)")
    df_imp = pd.DataFrame({'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Malasia', 'España'],
                           'MT': [750000, 680000, 520000, 290000, 85000]})
    fig_imp = px.bar(df_imp.sort_values('MT'), x='MT', y='País', orientation='h', color_discrete_sequence=['#800000'])
    st.plotly_chart(fig_imp, use_container_width=True)

# 7. PIE DE PÁGINA: AUTORÍA
st.markdown('<p class="footer-autor">Elaborado por: ELYMAR ESTÉVEZ</p>', unsafe_allow_html=True)
