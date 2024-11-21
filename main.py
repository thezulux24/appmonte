import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
from io import StringIO

key = st.secrets["key"]
def decrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

# Desencriptar y leer el DataFrame
decrypted_data = decrypt_file('data/data.csv', key)
df = pd.read_csv(StringIO(decrypted_data.decode()), delimiter=';')

st.title('Búsqueda Inscritos Carrera 4,2K Isla Bonita ')


search_option = st.radio('Seleccione el método de búsqueda', ('Cédula', 'Teléfono'))

resultado = None

if search_option == 'Cédula':
    cedula_input = st.text_input('Ingrese el número de cédula', '')
    if st.button('Buscar'):
        if cedula_input:
            resultado = df[df['Cedula'] == cedula_input]
        else:
            resultado = pd.DataFrame()
elif search_option == 'Teléfono':
    celular_input = st.text_input('Ingrese el número de teléfono', '')
    if st.button('Buscar'):
        if celular_input:
            resultado = df[df['Celular'] == celular_input]
        else:
            resultado = pd.DataFrame()

if resultado is not None:
    if not resultado.empty:
        st.success('Te encuentras inscrito.')
        st.toast('Te encuentras inscrito.', icon="✅")
        st.write(f"Nombre: {resultado.iloc[0]['Nombre']}")
        st.write(f"Apellido: {resultado.iloc[0]['Apellido']}")
        st.write(f"Categoria: {resultado.iloc[0]['Categoria']}")
        st.write(f"Sexo: {resultado.iloc[0]['Sexo']}")
        st.write(f"Talle: {resultado.iloc[0]['Talle']}")
    else:
        st.error('Cédula o teléfono no encontrado. No te encuentras inscrito.')
        st.toast('Cédula o teléfono no encontrado. No te encuentras inscrito.', icon="❌")