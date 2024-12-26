import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
from io import StringIO

# Configuración de la página
st.set_page_config(page_title="Búsqueda Inscritos Carrera", layout="centered")

key = st.secrets["key"]

def decrypt_file(file_name, key):
    try:
        f = Fernet(key)
        with open(file_name, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        st.error(f"Error al desencriptar: {str(e)}")
        return None

# Desencriptar y leer el DataFrame
decrypted_data = decrypt_file('data/data.csv', key)
if decrypted_data is not None:
    try:
        df = pd.read_csv(StringIO(decrypted_data.decode()), delimiter=';')
        df['Cedula'] = df['Cedula'].astype(str).str.strip()
        df['Celular'] = df['Celular'].astype(str).str.strip()
    except Exception as e:
        st.error(f"Error al leer datos: {str(e)}")
        st.stop()

st.title('Búsqueda Inscritos Carrera Cali 4,2K Donde Debes Estar')

search_option = st.radio('Seleccione el método de búsqueda', ('Cédula', 'Teléfono'))

resultado = None

if search_option == 'Cédula':
    cedula_input = st.text_input('Ingrese el número de cédula', '')
    if st.button('Buscar'):
        if cedula_input:
            cedula_input = str(cedula_input).strip()
            resultado = df[df["Cedula"].str.contains(cedula_input, case=False, na=False)]
        else:
            resultado = pd.DataFrame()

elif search_option == 'Teléfono':
    celular_input = st.text_input('Ingrese el número de teléfono', '')
    if st.button('Buscar'):
        if celular_input:
            celular_input = str(celular_input).strip()
            resultado = df[df['Celular'].str.contains(celular_input, case=False, na=False)]
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