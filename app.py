import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Cacao Corona")

# 2. ENCABEZADO CON LOGO Y TÍTULO
col_logo, col_titulo = st.columns([1, 4])

# Nombre exacto de tu archivo
nombre_logo = "logo_corona_bp.png"

with col_logo:
    # Verificamos si el archivo existe para evitar el error ValueError
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=180)
    else:
        # Si no lo encuentra, muestra un aviso pero permite que la app cargue
        st.warning(f"⚠️ No se encontró: {nombre_logo}")

with col_titulo:
    st.title("CUADRO DE MANDO - ESTRATEGIA CACAO")
    st.caption("Referencia de datos: Informe 13/01/2026")

st.divider()

# 3. FILA 1: MAPA MUNDIAL (Basado en tu PDF)
st.subheader("Concentración de la Producción Mundial (TM)")
data_mapa = {
    'País': ['Costa de Marfil', 'Ghana', 'Indonesia', 'Nigeria', 'Camerún', 'Brasil', 'Ecuador', 'Rep. Dominicana'],
    'ISO': ['CIV', 'GHA', 'IDN', 'NGA', 'CMR', 'BRA', 'ECU', 'DOM'],
    'Producción': [2100000, 800000, 650000, 300000, 280000, 200000, 150000, 80000]
}
df_mapa = pd.DataFrame(data_mapa)

fig_mapa = px.choropleth(df_mapa, 
    locations="ISO", 
    color="Producción",
    hover_name="País",
    color_continuous_scale=["#FADBD8", "#D35400", "#6E2C00"], # Tonos de naranja a marrón
    projection="natural earth"
)
fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
st.plotly_chart(fig_mapa, use_container_width=True)

# 4. FILA 2: GRÁFICOS DE MERCADO EN TIEMPO REAL
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Evolución de Precios Futuros (CC=F)")
    # Conexión directa a Yahoo Finance para actualización automática
    try:
        cacao_yf = yf.download("CC=F", period="1y")
        fig_precios = px.line(cacao_yf, y="Close", labels={'Close': 'Precio USD/MT', 'Date': 'Fecha'})
        fig_precios.update_traces(line_color='#D35400')
        st.plotly_chart(fig_precios, use_container_width=True)
    except:
        st.error("Error al conectar con los datos de mercado.")

with col_right:
    st.subheader("Comparativa de Producción por Origen")

with c3:
    st.markdown("### 🧬 Sanidad Vegetal")
    st.write("La enfermedad del brote hinchado amenaza gravemente la producción en los árboles de cacao.")
