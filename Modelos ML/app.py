# Este código es para usar con Streamlit + Streamlit Cloud
# Para ejecutar aplicación correr:
    # streamlit run app.py
# Para hacer deploy con Streamlit Cloud:
    # Sube tu código a GitHub.
    # Ve a Streamlit Cloud.
    # Conéctalo con tu repositorio de GitHub.
    # Elige el archivo app.py y despliega la aplicación.
# Link deployed app:
    # https://proyecto-final-lcinxctqprwitzzc46viuo.streamlit.app

import streamlit as st
import joblib
import pandas as pd
import os

# Definir la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "Modelos_ML")

# Cargar modelos y datos
def load_model(file_name):
    path = os.path.join(MODELS_DIR, file_name)
    return joblib.load(path)

def load_csv(file_name):
    path = os.path.join(MODELS_DIR, file_name)
    return pd.read_csv(path)

# Intentar cargar los modelos
try:
    modelo_sentimientos_final = load_model("modelo_sentimientos_final.pkl")
    vectorizer = load_model("vectorizador_tfidf.pkl")
    modelo_knn = load_model("modelo_knn.pkl")
    df = load_csv("data_recomendacion.csv")
except Exception as e:
    st.error(f"Error al cargar modelos o datos: {str(e)}")

# Asegurar que zip_code sea string
df['zip_code'] = df['zip_code'].astype(str)

# Configurar la app de Streamlit
st.title("🚀 API de Análisis de Comentarios y Recomendaciones de Restaurantes")

# Sección: Clasificación de Sentimientos
st.header("📝 Clasificación de Comentarios")
texto = st.text_input("Escribe un comentario para analizar su sentimiento:")

if st.button("Clasificar Comentario"):
    if texto:
        try:
            texto_tfidf = vectorizer.transform([texto])
            prediccion = modelo_sentimientos_final.predict(texto_tfidf)[0]
            
            # Asignar color según el sentimiento
            color = "green" if prediccion == "positivo" else "red" if prediccion == "negativo" else "gray"

            # Mostrar resultado con color
            st.markdown(f"""
                <div style="padding: 10px; background-color: {color}; color: white; border-radius: 5px; text-align: center;">
                    <b>El comentario tiene un sentimiento: {prediccion}</b>
                </div>
            """, unsafe_allow_html=True)        
        
        except Exception as e:
            st.error(f"Error en la predicción: {str(e)}")
    else:
        st.warning("Por favor, ingresa un comentario.")

# Sección: Recomendación de Restaurantes
st.header("🍽️ Recomendación de Restaurantes")

zip_code = st.text_input("Código postal:")
dia = st.selectbox("Día de la semana:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
hora = st.slider("Selecciona la hora (en formato decimal):", 0.0, 24.0, 12.0)

if st.button("Recomendar Restaurantes"):
    try:
        df_filtrado = df[df['zip_code'] == zip_code]

        if df_filtrado.empty:
            st.warning("No se encontraron restaurantes para ese código postal.")
        else:
            df_filtrado.loc[:, f'{dia}_open'] = pd.to_numeric(df_filtrado[f'{dia}_open'], errors='coerce')
            df_filtrado.loc[:, f'{dia}_close'] = pd.to_numeric(df_filtrado[f'{dia}_close'], errors='coerce')

            df_filtrado = df_filtrado[(df_filtrado[f'{dia}_open'] <= hora) & (df_filtrado[f'{dia}_close'] >= hora)]

            if df_filtrado.empty:
                st.warning("No hay restaurantes abiertos a esa hora.")
            else:
                top_10_reviews = df_filtrado.nlargest(10, 'num_of_reviews')
                top_5_rating = top_10_reviews.nlargest(5, 'avg_rating')

                for _, row in top_5_rating.iterrows():
                    st.write(f"**{row['name']}** - {row['street_address']} ({row['zip_code']})")
                    st.write(f"⭐ {row['avg_rating']} - {row['num_of_reviews']} opiniones")
                    st.markdown("---")
    except Exception as e:
        st.error(f"Error en la recomendación: {str(e)}")
