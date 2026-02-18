import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Cacao Pulse 360", page_icon="🍫")

# Estilos CSS
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }
    .main-header { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 20px; }
    .logo-container { max-width: 220px; height: auto; }
    .titulo-gigante { color: #800000; font-size: clamp(40px, 7vw, 90px); font-weight: 800; margin: 10px 0 0px 0; line-height: 1; letter-spacing: -2px; font-family: 'Segoe UI', sans-serif; text-transform: uppercase; }
    .subtitulo-inteligencia { color: #555555; font-size: 18px; font-weight: 500; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; }
    .footer-autor { text-align: center; color: #800000; font-weight: bold; font-size: 20px; margin-top: 50px; padding: 20px; border-top: 1px solid #eeeeee; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO CENTRADO
nombre_logo = "logo_corona_bp.png"
logo_html = ""
if os.path.exists(nombre_logo):
    with open(nombre_logo, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
        logo_html = f'<img src="data:image/png;base64,{data}" class="logo-container">'

st.markdown(f"""<div class="main-header">{logo_html}<h1 class="titulo-gigante">CACAO PULSE 360</h1><p class="subtitulo-inteligencia">Inteligencia de Mercado Global | Reporte 2026</p></div>""", unsafe_allow_html=True)

st.divider()

# 3. KPIs GLOBALES
k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.metric("Cacao Futuros (NY)", "3,203.00 USD", "-1.2%")
with k2: st.metric("Tasa EUR/USD", "1.0850", "-0.15%")
with k3: st.metric("Mín. 52 Semanas", "2,950.00", "")
with k4: st.metric("Máx. 52 Semanas", "11,722.00", "")
with k5: st.metric("Importación UE", "0.95M TM", "+0.2%")

st.divider()

# 4. ANÁLISIS DE DIVISAS Y PRECIOS (12 MESES)
col_eur, col_hist, col_fut = st.columns(3)

with col_eur:
    st.subheader("💱 Evolución EUR/USD (12M)")
    eur_data = {'Fecha': pd.date_range(end='2026-02-18', periods=12, freq='ME'),
                'EUR/USD': [1.08, 1.09, 1.07, 1.08, 1.10, 1.11, 1.12, 1.10, 1.09, 1.08, 1.085, 1.085]}
    fig_eur = px.line(pd.DataFrame(eur_data), x='Fecha', y='EUR/USD', markers=True)
    fig_eur.update_traces(line_color='#2ecc71')
    st.plotly_chart(fig_eur, use_container_width=True)

with col_hist:
    st.subheader("📉 Histórico Cacao USD/MT (12M)")
    # Reflejando la caída desde los máximos de 2024/2025 hacia los 3203 actuales
    hist_data = {'Fecha': pd.date_range(end='2026-02-18', periods=12, freq='ME'),
                 'Precio': [10500, 11700, 9800, 8500, 7200, 6400, 5800, 4900, 4100, 3500, 3100, 3203]}
    fig_hist = px.line(pd.DataFrame(hist_data), x='Fecha', y='Precio', markers=True)
    fig_hist.update_traces(line_color='#d35400')
    st.plotly_chart(fig_hist, use_container_width=True)

with col_fut:
    st.subheader("📅 Mercado de Futuros USD/MT (12M)")
    # Proyección a 12 meses vista desde Mar 26
    venc_data = {'Mes': ['Mar 26', 'May 26', 'Jul 26', 'Sep 26', 'Dic 26', 'Mar 27', 
                        'May 27', 'Jul 27', 'Sep 27', 'Dic 27', 'Mar 28', 'May 28'],
                 'Precio': [3203, 3190, 3175, 3160, 3140, 3110, 3090, 3075, 3050, 3020, 2990, 2970]}
    fig_venc = px.line(pd.DataFrame(venc_data), x='Mes', y='Precio', markers=True, text='Precio')
    fig_venc.update_traces(line=dict(color='#7e3412', width=3), textposition="top center")
    st.plotly_chart(fig_venc, use_container_width=True)

st.divider()

# 5. PRODUCCIÓN Y STOCKS
col_prod, col_stock_p = st.columns([2, 1])
df_prod = pd.DataFrame({
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU'],
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000],
    'Exportación': [1650000, 620000, 410000, 210000, 190000, 10000, 145000],
    'Stocks': [450000, 180000, 120000, 65000, 55000, 40000, 35000]
})

with col_prod:
    st.subheader("📍 Concentración de la Producción Mundial")
    fig_map = px.choropleth(df_prod, locations="ISO", color="Producción", color_continuous_scale="Oranges", projection="orthographic")
    fig_map.update_geos(projection_rotation=dict(lon=0, lat=10, roll=0), showocean=True, oceancolor="#e8f4f8")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

with col_stock_p:
    st.subheader("📦 Stocks en Origen (MT)")
    st.plotly_chart(px.bar(df_prod.sort_values('Stocks'), x='Stocks', y='País', orientation='h', color='Stocks', color_continuous_scale='Reds'), use_container_width=True)

st.divider()

# 6. EXPORTACIONES, CONSUMO E IMPORTADORES
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("🚢 Exportaciones (MT)")
    st.plotly_chart(px.bar(df_prod.sort_values('Exportación'), x='Exportación', y='País', orientation='h', color_discrete_sequence=['#d35400']), use_container_width=True)
with c2:
    st.subheader("☕ Consumidores (MT)")
    df_c = pd.DataFrame({'País': ['EE.UU.', 'Alemania', 'Francia', 'Reino Unido', 'España'], 'MT': [795000, 380000, 245000, 210000, 88000]})
    st.plotly_chart(px.bar(df_c.sort_values('MT'), x='MT', y='País', orientation='h', color_discrete_sequence=['#a04000']), use_container_width=True)
with c3:
    st.subheader("📥 Importadores (MT)")
    df_i = pd.DataFrame({'País': ['Países Bajos', 'EE.UU.', 'Alemania', 'Malasia', 'España'], 'MT': [750000, 680000, 520000, 290000, 85000]})
    st.plotly_chart(px.bar(df_i.sort_values('MT'), x='MT', y='País', orientation='h', color_discrete_sequence=['#800000']), use_container_width=True)

# 7. PIE DE PÁGINA
st.markdown('<p class="footer-autor">Elaborado por: ELYMAR ESTÉVEZ</p>', unsafe_allow_html=True)
