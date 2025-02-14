# Proyecto de Análisis de Sentimientos y Dashboard para Apertura de Restaurante de Pizza

## Introducción

EEUU, junto a México y Canadá, organizará el Mundial de futbol 2026. Un evento único en el mundo que mueve más de 3 millones de espectadores y 3.5 billones de televidentes (fuente: FIFA). Siendo el Metlife Stadium con una capacidad de 82.500 personas sede de siete partidos distribuidos en cuatro de fase de grupos, uno de 16vos de final, uno de 4tos de final y sobre todo el más importante, la final, el objetivo principal de este proyecto es Recomendar una ubicación en los alrededores del estadio para la apertura de un local de pizzas, a esto añadimos que según el último Censo realizado por Estados Unidos New York ocupa el cuarto lugar entre los estados con mayores ingresos por concepto de restaurantes de servicio limitado y New Jearsey entre dentro del Top 15 en este concepto.

## Objetivos del Proyecto

- Recomendar una ubicación para la apertura de un nuevo restaurante de pizza en el estado de Nueva Jersey, en las inmediaciones del Metlife Stadium.

- Crear un Dashboard en Power BI que permita visualizar KPIs relacionados con las reviews plasmadas en Google Maps y las puntuaciones de la experiencia de los clientes.

- Crear un sistema de recomendación de restaurante para los clientes en la zona de New Jearsey.

## Datos Utilizados

Los datos empleados han sido extraídos de las siguientes fuentes:

- Google Maps

- Yelp

- API de loopnet para conocer la disponibilidad de locales en las zonas aledañas al estadio.

## Tecnologías Utilizadas

Para nuestro proyecto, elegimos un stack tecnológico basado en AWS, ya que nos permite escalabilidad, automatización y optimización de costos sin necesidad de gestionar infraestructura propia.
Para la fuente de datos, utilizamos datasets de Yelp y Google Maps, almacenándolos en Amazon S3 en formatos JSON y Parquet, lo que nos permite manejar grandes volúmenes de datos de manera eficiente y reducir costos de almacenamiento.
El procesamiento de datos lo realizaremos con AWS Glue, que nos permite ejecutar procesos ETL para luego cargarlos en Amazon RDS que será nuestra base de datos relacional optimizada para consultas SQL rápidas. Además, utilizaremos Pandas y NumPy para análisis exploratorio. 
Para la automatización, optamos por AWS Lambda, lo que nos permite orquestar flujos de trabajo de Glue y RDS de manera automática sin servidores.
En la parte de Machine Learning, utilizaremos Scikit-learn para modelos predictivos y de análisis de sentimiento, optimizando el proceso de toma de decisiones basado en datos y spaCy para procesamiento de lenguaje natural
Por último, para la visualización y despliegue, usaremos Power BI para dashboards interactivos y Streamlit para crear aplicaciones dinámicas y accesibles.
Este stack nos permite un flujo de datos completamente automatizado, optimizando la ingesta, transformación, almacenamiento y análisis, asegurando eficiencia y escalabilidad en la nube.

![Stack](<Assets/Stack Tecnológico.png>)

## KPIs

Se emplearán 3 KPIs principales para evaluar el éxito del proyecto:

- Crecimiento trimestral de 2% en el número de reviews para la cadena en los estados estudiados. Su fórmula es la siguiente:

$`KPI = ((Reviews Nuevos - Reviews Actual) / Reviews Actual) * 100`$

- Incremento trimestral de 0.1 puntos en la valoración de los establecimientos en los estados de Nueva York y Nueva Jersey. Su fórmula es la siguiente:

$`KPI = Valoración Nueva - Valoración Actual`$

- Aumentar la proporción trimestral de comentarios positivos en 3% de los establecimientos. Su fórmula es la siguiente:

$`KPI = (((Comentarios Positivos Nuevos- Comentarios Negativos Nuevos) - (Comentarios Positivos Actuales - Comentarios Negativos Actuales))/ (Comentarios Positivos Actuales - Comentarios Negativos Actuales)) * 100`$


## Hallazgos Preliminares

- El promedio de calificaciones para las pizzerías de los estados de New Jearsey y New York es de 4.11. El rango de calificación se encuentra entre 1 y 5.

- Los locales tienen en promedio 89.9 reviews cada uno. El que más riviews posee 4362 reviews.

- Pizza Hut la cadena en que se enfoca este proyecto tiene un promedio de calificación de 3.3 en New Jearsey y 3.7 en New York.

- A continuación se puede observar la relación entre la cantidad de reviews en Google Map y el promedio de calificaciones, destacando que a mayor número de reviews menor es el número de calificaciones.

![Reviews](<Assets/Relación Reviews - Puntuaciones.png>)
