from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd

# Inicializar FastAPI
app = FastAPI()

# Cargar el modelo de análisis de sentimientos
modelo_sentimientos_final = joblib.load(r'C:\Users\guard\OneDrive\Desktop\Henry Data Science\Proyecto-FInal\Modelos ML\modelo_sentimientos_final.pkl')
vectorizer = joblib.load(r'C:\Users\guard\OneDrive\Desktop\Henry Data Science\Proyecto-FInal\Modelos ML\vectorizador_tfidf.pkl')

# Cargar modelo y datos para recomendaciones
modelo_knn = joblib.load(r'C:\Users\guard\OneDrive\Desktop\Henry Data Science\Proyecto-FInal\Modelos ML\modelo_knn.pkl')
df_binarias = pd.read_csv(r'C:\Users\guard\OneDrive\Desktop\Henry Data Science\Proyecto-FInal\Modelos ML\data_preprocesada.csv')

# Clase para el cuerpo de la petición de análisis de sentimientos
class Comentario(BaseModel):
    texto: str

# Clase para el cuerpo de la petición de recomendaciones
class Consulta(BaseModel):
    horario: str
    condiciones_binarias: List[int]
    zip_code: str

# Endpoint para análisis de sentimientos
@app.get("/clasificar_comentario")
def clasificar_comentario(texto: str):
    # Vectorizar el comentario
    texto_tfidf = vectorizer.transform([texto])
    # Predecir el sentimiento
    prediccion = modelo_sentimientos_final.predict(texto_tfidf)[0]
    return {"sentimiento": prediccion}

# Endpoint para recomendar locales
@app.get("/recomendar_locales")
def recomendar_locales(
    horario: str = Query(..., description="Horario en formato 'HH:MM-HH:MM'"),
    delivery: Optional[int] = Query(0, ge=0, le=1, description="1 si el local tiene entrega a domicilio, 0 si no"),
    dine_in: Optional[int] = Query(0, ge=0, le=1, description="1 si el local tiene opción para comer en el lugar, 0 si no"),
    takeout: Optional[int] = Query(0, ge=0, le=1, description="1 si el local tiene opción para llevar, 0 si no"),
    good_for_kids: Optional[int] = Query(0, ge=0, le=1, description="1 si el local es adecuado para niños, 0 si no"),
    casual: Optional[int] = Query(0, ge=0, le=1, description="1 si el local tiene ambiente casual, 0 si no"),
    dinner: Optional[int] = Query(0, ge=0, le=1, description="1 si el local sirve cenas, 0 si no"),
    lunch: Optional[int] = Query(0, ge=0, le=1, description="1 si el local sirve almuerzos, 0 si no"),
    zip_code: str = Query(..., description="Código postal de la ubicación del usuario")
):
    # Convertir horario a formato de 24 horas
    try:
        horario_inicio, horario_fin = horario.split('-')
    except ValueError:
        return {"error": "Formato de horario inválido. Usa 'HH:MM-HH:MM'."}
    
    # Filtrar locales abiertos en el horario especificado y por código postal
    df_filtrado = df_binarias[df_binarias['zip_code'] == zip_code]
    
    # Crear vector de consulta
    consulta = [delivery, dine_in, takeout, good_for_kids, casual, dinner, lunch]
    
    while len(consulta) < 21:
        consulta.append(0)  # Agrega un valor predeterminado (0 en este caso) para las características faltantes
    
    consulta = pd.Series(consulta).values.reshape(1, -1)
    
    # Encontrar vecinos más cercanos
    distancias, indices = modelo_knn.kneighbors(consulta)
    recomendaciones = df_filtrado.iloc[indices[0]]
    
    # Ordenar por num_of_reviews y avg_rating
    recomendaciones = recomendaciones.sort_values(by=['num_of_reviews', 'avg_rating'], ascending=[False, False])
    return recomendaciones[['name', 'avg_rating', 'num_of_reviews', 'latitude', 'longitude', 'zip_code']].to_dict(orient='records')
