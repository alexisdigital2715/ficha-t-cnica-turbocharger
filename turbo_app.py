import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Ficha Técnica Turbocharger", layout="centered")

# Título
st.title("📋 Ficha Técnica de Inspección")
st.markdown("---")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# Esto busca las credenciales que guardaste en Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para cargar datos actuales
def cargar_datos():
    try:
        return conn.read(worksheet="Hoja 1", usecols=list(range(10)), ttl=5)
    except Exception:
        return pd.DataFrame()

# --- MENÚ LATERAL ---
menu = st.sidebar.selectbox(
    "Selecciona el Módulo",
    ["Nueva Inspección", "Historial en la Nube"]
)

if menu == "Nueva Inspección":
    st.header("🔧 Registrar Nuevo Turbo")
    
    col1, col2 = st.columns(2)
    with col1:
        operador = st.text_input("Técnico Responsable")
    with col2:
        modelo = st.text_input("Modelo del Turbo")
        horas = st.number_input("Horas de trabajo", min_value=0)

    st.subheader("1. Estado Físico")
    col_a, col_b = st.columns(2)
    with col_a:
        visual = st.selectbox("Inspección Visual", ["OK", "Golpes/Rajaduras", "Suciedad"])
        ingreso_aceite = st.selectbox("Ingreso Aceite", ["No", "Sí"])
    with col_b:
        juego_axial = st.number_input("Juego AXIAL (mm)", format="%.3f")
        juego_radial = st.number_input("Juego RADIAL (mm)", format="%.3f")

    retorno_aceite = st.selectbox("Retorno de Aceite", ["Fluido", "Obstruido"])
    comentarios = st.text_area("Observaciones")

    if st.button("☁️ GUARDAR EN LA NUBE"):
        if not operador or not modelo:
            st.warning("⚠️ Por favor ingresa el nombre del técnico y modelo.")
        else:
            # 1. Crear la fila nueva
            nuevo_dato = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Técnico": operador,
                "Modelo": modelo,
                "Horas": horas,
                "Visual": visual,
                "Juego Axial": juego_axial,
                "Juego Radial": juego_radial,
                "Ingreso Aceite": ingreso_aceite,
                "Retorno Aceite": retorno_aceite,
                "Comentarios": comentarios
            }])

            # 2. Descargar datos viejos + Unir con el nuevo
            try:
                datos_existentes = cargar_datos()
                datos_actualizados = pd.concat([datos_existentes, nuevo_dato], ignore_index=True)
                
                # 3. Subir todo a Google Sheets
                conn.update(worksheet="Hoja 1", data=datos_actualizados)
                
                st.success("✅ ¡Guardado exitosamente en Google Drive!")
                st.balloons()
            except Exception as e:
                st.error(f"Error al conectar con la hoja: {e}")

elif menu == "Historial en la Nube":
    st.header("📂 Base de Datos en Vivo")
    st.info("Estos datos vienen directamente de tu Google Sheet.")
    
    # Botón para refrescar datos manualmente
    if st.button("🔄 Actualizar Tabla"):
        st.cache_data.clear()
    
    try:
        df = cargar_datos()
        st.dataframe(df)
    except Exception as e:
        st.error("No se pudo cargar la hoja. Verifica que el nombre de la hoja en el Excel sea 'Hoja 1'.")
