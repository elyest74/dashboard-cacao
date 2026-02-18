import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

st.set_page_config(layout="wide", page_title="Dashboard Cacao Corona")

# ENCABEZADO
col_logo, col_titulo = st.columns([1, 4])
nombre_logo = "logo_corona_bp.png"

with col_logo:
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        st.warning(f"⚠️ No se encontró: {nombre_logo}")

with col_titulo:
    st.title("CUADRO DE MANDO - ESTRATEGIA CACAO")
    st.caption("Referencia de datos: Informe 13/01/2026")

st.divider()

# FILA 1: MAPA
st.subheader("Concentración de la Producción Mundial (TM)")
data_mapa = {
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador', 'Rep. Dominicana'],
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU', 'DOM'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000, 80000]
}
df_mapa = pd.DataFrame(data_mapa)
fig_mapa = px.choropleth(df_mapa, locations="ISO", color="Producción", hover_name="País",
    color_continuous_scale=["#FADBD8", "#D35400", "#6E2C00"], projection="natural earth")
fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
st.plotly_chart(fig_mapa, use_container_width=True)

# FILA 2: MERCADO Y COMPARATIVA
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Evolución de Precios Futuros (CC=F)")
    try:
        # Usamos un método más robusto para obtener datos
        cacao_data = yf.download("CC=F", period="1y", interval="1d", progress=False)
        if not cacao_data.empty:
            fig_precios = px.line(cacao_data, y="Close")
            fig_precios.update_traces(line_color='#D35400')
            st.plotly_chart(fig_precios, use_container_width=True)
        else:
            st.info("Buscando datos de mercado...")
    except:
        st.error("Error de conexión con Yahoo Finance.")

with col_right:
    st.subheader("Comparativa de Producción por Origen")
    fig_barras = px.bar(df_mapa.sort_values('Producción', ascending=True), 
                        x='Producción', y='País', orientation='h',
                        color_discrete_sequence=['#D35400'])
    st.plotly_chart(fig_barras, use_container_width=True)

# FILA 3: RIESGOS
st.divider()
st.subheader("Factores Críticos de Decisión 2026")
c1, c2, c3 = st.columns(3)
with c1:
    st.error("🚨 **RIESGO CLIMÁTICO**")
    st.write("Déficit hídrico en África Occidental. Costa de Marfil bajo vigilancia.")
with c2:
    st.warning("⚖️ **REGULACIÓN EUDR**")
    st.write("Diciembre 2025: Normativa de deforestación activa.")
with c3:
    st.info("📊 **STOCKS**")
    st.write("Caída en inventarios certificados presionando precios.")
