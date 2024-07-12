import streamlit as st
import pandas as pd

df = pd.read_csv('data/data.csv', delimiter=';')

st.title('Búsqueda Inscritos Carrera 4,2K Híbrida')

cedula_input = st.text_input('Ingrese el número de cédula', '')

if st.button('Buscar'):
    # Filtrar el DataFrame para encontrar la cédula
    resultado = df[df['Cedula'] == cedula_input]

    if not resultado.empty:
        st.write(f"Nombre: {resultado.iloc[0]['Nombres']}")
        st.write(f"Apellidos: {resultado.iloc[0]['Apellidos']}")
        st.write(f"Género: {resultado.iloc[0]['Genero']}")
        st.write(f"Talla de camiseta: {resultado.iloc[0]['Talla de la camisa']}")
    else:
        st.error('Cédula no encontrada.')