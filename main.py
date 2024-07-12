import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
from io import StringIO

# Cargar la clave de cifrado desde .streamlit/secrets.toml
key = st.secrets["encryption_key"].encode()

# Función para desencriptar el archivo
def decrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

# Desencriptar y leer el DataFrame
decrypted_data = decrypt_file('data/data.csv', key)
df = pd.read_csv(StringIO(decrypted_data.decode()), delimiter=';')

# La lógica de la aplicación sigue aquí...
st.title('Búsqueda Inscritos Carrera 4,2K Híbrida')

cedula_input = st.text_input('Ingrese el número de cédula', '')

if st.button('Buscar'):
    resultado = df[df['Cedula'] == cedula_input]
    if not resultado.empty:
        st.write(f"Nombre: {resultado.iloc[0]['Nombres']}")
        st.write(f"Apellidos: {resultado.iloc[0]['Apellidos']}")
        st.write(f"Género: {resultado.iloc[0]['Genero']}")
        st.write(f"Talla de camiseta: {resultado.iloc[0]['Talla de la camisa']}")
    else:
        st.error('Cédula no encontrada.')