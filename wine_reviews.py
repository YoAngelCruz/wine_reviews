import streamlit as st
import pandas as pd
import numpy as np
import codecs
import plotly.express as px

st.title('Wine-reviews app')
##Credencial
st.sidebar.image("logo.png")
st.sidebar.markdown("##")
##Nombre y matricula
st.header("Angel Moises Cruz Cruz")
st.markdown("S19004906")

URL='winer.csv'

@st.cache
def load_data(nrows):
    doc = codecs.open(URL,'r','latin1')
    data = pd.read_csv(doc, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    return data

def filter_data_by_variety(variety):
    filtered_data_variety = data[data['variety'].str.upper().str.contains(variety)]
    return filtered_data_variety

def filter_data_by_taster(taster):
    filtered_data_taster = data[data['taster_name'] == taster]
    return filtered_data_taster


data_load_state = st.text('Cargando...')
data = load_data(10000)
data_load_state.text("Done Angel Cruz! (using st.cache)")

if st.sidebar.checkbox('Mostrar todas las reseñas'):
    st.subheader('Todas las reseñas')
    st.write(data)


orCountry = st.sidebar.text_input('Nombre de la variedad :')
Buscar = st.sidebar.button('Buscar variedad')

if (Buscar):
   data_country = filter_data_by_variety(orCountry.upper())
   count_row = data_country.shape[0]  
   st.write(f"Resultados encontrados: {count_row}")
   st.write(data_country)



selected_taster = st.sidebar.selectbox("Seleccionar Catador", data['taster_name'].unique())
FilterbyDirector = st.sidebar.button('Filtrar catador ')

if (FilterbyDirector):
   filterbydir = filter_data_by_taster(selected_taster)
   count_row = filterbydir.shape[0] 
   st.write(f"Resultados para filtro de Catadores: {count_row}")

   st.dataframe(filterbydir)

ranges = [(80, 84), (85, 89), (90, 94), (95, 100)]
labels = ['80-84', '85-89', '90-94', '95-100']

hist_data = {label: [] for label in labels}

for r in ranges:
    hist_data[f"{r[0]}-{r[1]}"] = data[(data['points'] >= r[0]) & (data['points'] <= r[1])]['points'].count()

st.sidebar.markdown("##")
st.sidebar.markdown("Diagramas")


# Histograma 
if st.sidebar.checkbox('Rangos de puntos'):
    st.markdown("Histograma para analizar las puntaje mas fuecuentes entre las criticas de vinos")
    fig_histogram = px.bar(x=labels, 
                       y=[hist_data[label] for label in labels],
                       title="Rangos de puntaje mas frecuentes",
                       labels={'x': 'Rango de puntuaciones', 'y': 'Frecuencia de datos'})
    st.plotly_chart(fig_histogram, use_container_width=True)

# grafica de dos entradas

if st.sidebar.checkbox('Variedad por país'):
    st.markdown("Diagrama para analizar los diferentes tipos de vino elaborados por cada país")
    grouped_data = data.groupby(['country', 'variety']).size().reset_index(name='counts')
    fig_graph2 = px.bar(grouped_data, 
                    x='country', 
                    y='counts', 
                    color='variety', 
                    title='Variedad de vinos por país')
    st.plotly_chart(fig_graph2, use_container_width=True)

# grafica de scatter 

if st.sidebar.checkbox('scatter'):
    st.markdown("Diagrama que visualiza como entre mas alta la calificacion, mas aumenta el precio del vino")
    fig = px.scatter(data, x='price', 
                     y='points', 
                     color='variety', 
                     hover_name='country', 
                     title='Precio vs. Puntuación por variedad')
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)