import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

spark = SparkSession.builder.appName("WeatherDashboard").getOrCreate()

try:
    anomalies = spark.read.json("hdfs://namenode:9000/hdfs-data/anomalies").toPandas()
except AnalysisException:
    anomalies = pd.DataFrame(columns=["city", "country", "event_time", "variable", "observed_value", "expected_value", "anomaly_type"])

try:
    seasonal = spark.read.json("hdfs://namenode:9000/hdfs-data/seasonal_profile_enriched").toPandas()
except Exception:
    seasonal = pd.DataFrame()

try:
    history = spark.read.json("hdfs://namenode:9000/hdfs-data/weather_history_raw").limit(10000).toPandas()
except Exception:
    history = pd.DataFrame()

st.title("Dashboard Global de Visualisation Météo")

st.header("Anomalies Détectées")
if not anomalies.empty:
    st.dataframe(anomalies[["city", "country", "event_time", "variable", "observed_value", "expected_value", "anomaly_type"]].head(10))

    fig1 = pd.value_counts(anomalies['anomaly_type']).plot(kind='bar', title="Nombre d'anomalies par type").get_figure()
    st.pyplot(fig1)

    if 'city' in anomalies.columns:
        fig2 = pd.value_counts(anomalies['city']).plot(kind='bar', title="Anomalies par ville").get_figure()
        st.pyplot(fig2)
else:
    st.write("Aucune anomalie détectée pour le moment.")

st.header("Profils Saisonniers")
if not seasonal.empty:
    cities = seasonal['city'].unique()
    selected_city = st.selectbox("Sélectionnez une ville", cities)

    city_data = seasonal[seasonal['city'] == selected_city]
    
    st.subheader(f"Température moyenne mensuelle - {selected_city}")
    st.line_chart(city_data.set_index('month')['avg_temperature'])

    st.subheader(f"Vitesse du vent moyenne - {selected_city}")
    st.line_chart(city_data.set_index('month')['avg_windspeed'])
else:
    st.write("Données saisonnières non disponibles.")

st.header("Données Historiques")
if not history.empty and 'temperature' in history.columns:
    history['event_time'] = pd.to_datetime(history['event_time'], errors='coerce')
    history = history.dropna(subset=['event_time']).sort_values('event_time')

    st.subheader("Évolution de la température (derniers points)")
    st.line_chart(history.set_index('event_time')['temperature'].tail(200))
else:
    st.write("Données historiques non disponibles.")
