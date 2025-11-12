import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

spark = SparkSession.builder.appName("WeatherDashboard").getOrCreate()

try:
    anomalies = spark.read.json("hdfs://namenode:9000/hdfs-data/anomalies").toPandas()
except AnalysisException as e:
    if "PATH_NOT_FOUND" in str(e):
        anomalies = pd.DataFrame(columns=["city", "country", "event_time", "variable", "observed_value", "expected_value", "anomaly_type"])
    else:
        raise e

seasonal = spark.read.json("hdfs://namenode:9000/hdfs-data/seasonal_profile_enriched").toPandas()

st.title("Dashboard Global de Visualisation Météo")

st.header("Anomalies en temps réel")
if not anomalies.empty:
    st.dataframe(anomalies[["city", "country", "event_time", "variable", "observed_value", "expected_value", "anomaly_type"]].head(10))
else:
    st.write("Aucune anomalie détectée pour le moment.")

st.header("Profil saisonnier - Paris")
paris_data = seasonal[seasonal["city"] == "Paris"]
if not paris_data.empty:
    st.line_chart(paris_data.set_index("month")["avg_temperature"])
else:
    st.write("Aucune donnée saisonnière disponible pour Paris.")