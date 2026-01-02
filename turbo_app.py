import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Ficha Técnica Turbocharger", layout="centered")

st.title("📋 Ficha Técnica de Inspección Turbocharger")
st.markdown("---")

# --- MENÚ LATERAL ---
menu = st.sidebar.selectbox(
    "Selecciona el Módulo",
    ["Mantenimiento Preventivo", "Historial de Registros", "Diagnóstico Inteligente"]
)

if menu == "Mantenimiento Preventivo":
    st.header("🔧 Nueva Inspección Técnica")
    
    col1, col2 = st.columns(2)
    with col1:
        operador = st.text_input("Técnico Responsable", "Mecánico Turno 1")
    with col2:
        modelo = st.text_input("Modelo del Turbo", "G3520C")
        horas = st.number_input("Horas de trabajo", min_value=0)

    st.subheader("1. Estado Físico y Lubricación")
    col_a, col_b = st.columns(2)
    with col_a:
        visual = st.selectbox("Inspección Visual", ["OK", "Golpes/Rajaduras", "Suciedad Excesiva"])
        ingreso_aceite = st.radio("Ingreso Aceite", ["Sí", "No"], horizontal=True)
    with col_b:
        fugas = st.selectbox("Fugas de Gases", ["No", "Leves", "Criticas"])
        retorno_aceite = st.radio("Retorno Aceite", ["Fluido", "Obstruido"], horizontal=True)

    st.subheader("2. Metrología (Juegos del Eje)")
    col_med1, col_med2 = st.columns(2)
    with col_med1:
        axial = st.number_input("Juego AXIAL (mm)", format="%.3f", step=0.01)
    with col_med2:
        radial = st.number_input("Juego RADIAL (mm)", format="%.3f", step=0.01)

    comentarios = st.text_area("Observaciones Adicionales:")

    if st.button("💾 GUARDAR INSPECCIÓN EN EXCEL"):
        # Crear la fila de datos
        datos_nuevos = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Técnico": operador,
            "Modelo": modelo,
            "Horas": horas,
            "Visual": visual,
            "Juego Axial": axial,
            "Juego Radial": radial,
            "Ingreso Aceite": ingreso_aceite,
            "Retorno Aceite": retorno_aceite,
            "Comentarios": comentarios
        }
        
        # Guardar en archivo CSV (Excel)
        archivo = "reporte_turbos.csv"
        df_nuevo = pd.DataFrame([datos_nuevos])
        
        if not os.path.exists(archivo):
            df_nuevo.to_csv(archivo, index=False)
        else:
            df_nuevo.to_csv(archivo, mode='a', header=False, index=False)
            
        st.success("✅ ¡Inspección guardada correctamente en la PC!")

elif menu == "Historial de Registros":
    st.header("📂 Historial Guardado")
    archivo = "reporte_turbos.csv"
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        st.dataframe(df) # Muestra la tabla interactiva
    else:
        st.info("Aún no hay registros guardados.")

elif menu == "Diagnóstico Inteligente":
    st.header("🧠 Asistente de Fallas")
    sintoma = st.selectbox("Síntoma", ["Seleccionar...", "Humo Azul", "Humo Negro", "Ruido Metálico"])
    if sintoma == "Humo Azul":
        st.warning("Posible paso de aceite por sellos.")
    elif sintoma == "Ruido Metálico":
        st.error("¡Parar Motor! Posible roce de álabes.")