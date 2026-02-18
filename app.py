import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# Configuración de página
st.set_page_config(layout="wide", page_title="Cacao Global Dashboard")

st.title("🍫 Cuadro de Mando: Mercado del Cacao 2026")

# --- DATOS DE PRODUCCIÓN (Basados en tu informe) ---
# Usamos códigos ISO de 3 letras para que el mapa reconozca los países
data_mapa = {
    'País': ['Ivory Coast', 'Ghana', 'Indonesia', 'Nigeria', 'Cameroon', 'Brazil', 'Ecuador', 'Dominican Republic'],
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU', 'DOM'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000, 80000]
}
df_mapa = pd.DataFrame(data_mapa)

# --- MAPA MUNDIAL INTERACTIVO ---
st.subheader("Concentración de la Producción Mundial (TM)")
fig_mapa = px.choropleth(df_mapa, 
    locations="ISO", 
    color="Producción",
    hover_name="País",
    color_continuous_scale=["#ffe5d9", "#d35400", "#7e3412"], # Tonos de naranja fuerte a marrón cacao
    projection="natural earth"
)

fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
st.plotly_chart(fig_mapa, use_container_width=True)

# --- RESTO DEL DASHBOARD EN COLUMNAS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Evolución de Precios (USD/MT)")
    ticker = "CC=F"
    cacao_data = yf.download(ticker, period="1y")
    fig_precios = px.line(cacao_data, y="Close", labels={'Close': 'Precio', 'Date': 'Fecha'})
    fig_precios.update_traces(line_color='#d35400')
    st.plotly_chart(fig_precios, use_container_width=True)

with col2:
    st.subheader("Riesgos Clave 2026")
    st.info("**Clima:** Impacto en África Occidental por sequías[cite: 37, 41].")
    st.warning("**Regulación:** Normativa EUDR activa en Dic 2025[cite: 119].")
    st.error("**Sanidad:** Riesgo por virus del 'brote hinchado'[cite: 118].")
