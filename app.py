import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard Cacao 2026")

# 2. ENCABEZADO: LOGO Y TÍTULO
# Hemos ajustado el nombre al archivo exacto que tienes en GitHub
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    try:
        # Aquí es donde ponemos el nombre exacto de tu archivo
        st.image("logo_corona_bp.png", width=150) 
    except:
        st.error("No se pudo cargar 'logo_corona_bp.png'. Revisa que esté en la raíz de tu GitHub.")

with col_titulo:
    st.title("CUADRO DE MANDO - CACAO")
    st.caption("Actualizado: 13/01/2026")

st.divider()

# 3. FILA 1: MAPA MUNDIAL DE PRODUCCIÓN
st.subheader("Concentración de la Producción Mundial (TM)")
# Datos basados en tu informe
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
    color_continuous_scale=["#ffe5d9", "#d35400", "#7e3412"],
    projection="natural earth"
)
fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
st.plotly_chart(fig_mapa, use_container_width=True)

# 4. FILA 2: GRÁFICOS COMPARATIVOS Y PRECIOS
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Producción por País (TM)")
    # Replicando los datos del gráfico de barras del PDF
    fig_prod = px.bar(df_mapa.sort_values('Producción', ascending=False), 
                      x='País', y='Producción', 
                      color_discrete_sequence=['#d35400'])
    st.plotly_chart(fig_prod, use_container_width=True)

with col_right:
    st.subheader("Evolución de Precios Futuros (€/MT)")
    # Conexión real a mercado (CC=F es Cacao)
    cacao_yf = yf.download("CC=F", period="1y")
    fig_precios = px.line(cacao_yf, y="Close")
    fig_precios.update_traces(line_color='#d35400')
    st.plotly_chart(fig_precios, use_container_width=True)

# 5. FILA 3: PREVISIONES Y RIESGOS
st.divider()
st.subheader("Análisis de Riesgos y Regulaciones")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### ☁️ Clima 2026")
    st.write("Se espera que el cambio climático afecte negativamente la producción en África Occidental. Hasta el 50% de las áreas en Costa de Marfil podrían perderse para 2060.")

with c2:
    st.markdown("### 📜 Regulación EUDR")
    st.write("La entrada en vigor de la EUDR en diciembre de 2025 impactará los costos de trazabilidad y precios.")

with c3:
    st.markdown("### 🧬 Sanidad Vegetal")
    st.write("La enfermedad del brote hinchado amenaza gravemente la producción en los árboles de cacao.")
