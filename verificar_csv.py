import pandas as pd
from tabulate import tabulate
import textwrap
import os

# Cargar los archivos CSV
#archivo1 = 'archivos/LEGAJO_20240430CCS 2 - copia.csv'
archivo1 = 'archivos/LEGAJO_20240430CVG_2 2.csv'
archivo2 = 'archivos/LEGAJO_20240430CCS 2.csv'

#Extraemos el nombre de los archivos
nombre_archivo1 = os.path.basename(archivo1)
nombre_archivo2 = os.path.basename(archivo2)

#Definios los dataFrames para manipular los datos
df1 = pd.read_csv(archivo1)
df2 = pd.read_csv(archivo2)

# Inicializar resultados
resultados = []

# Regla: Verifica si los nombres de las columnas son iguales
def verifica_nombre_columnas(df1, df2):
    if list(df1.columns) == list(df2.columns):
        return "Las columnas son iguales", True
    else:
        mensaje = (
            "Las columnas son diferentes\n"
            f"  ====>{nombre_archivo1}:\n{list(df1.columns)}\n"
            f"  ====>{nombre_archivo2}:\n{list(df2.columns)}"
        )
        return mensaje, False
    
# Regla: verifica si la cantidad de columnas son iguales
def verifica_cantidad_columnas(df1, df2):
    if len(df1.columns) == len(df2.columns):
        return "Las columnas tienen la misma cantidad", True
    else:
        return "El número de columnas es distinto", False

# Regla: Verifica si el numero de filas son iguales
def verifica_cantidad_filas(df1, df2):
    if len(df1) == len(df2):
        return "El número de filas es igual", True
    else:
        mensaje = (
            "El número de filas es diferente\n"
            f"  ====>{nombre_archivo1}: {len(df1)} filas\n"
            f"  ====>{nombre_archivo2}: {len(df2)} filas"
        )
        return mensaje, False

# Regla: Verifica que una columna sea un número con dos decimales
def verifica_columna_format_monto(df1, df2, columna):
    def es_numero_con_dos_decimales(valor):
        try:
            return round(float(valor), 2) == float(valor)
        except ValueError:
            return False
    mensaje = []
    resultado = True
    for df, nombre_archivo in zip([df1, df2], [nombre_archivo1, nombre_archivo2]):
        if columna not in df.columns:
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' no existe")
            resultado = False
        elif not df[columna].apply(es_numero_con_dos_decimales).all():
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' no tiene un número con dos decimales")
            resultado = False
        else:
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' superó la validación")
    return "\n".join(mensaje), resultado

# Regla: Verificar que una columna tenga una longitud específica
def verifica_columna_longitud(df1, df2, columna, longitud):
    mensaje = []
    resultado = True
    for df, nombre_archivo in zip([df1, df2], [nombre_archivo1, nombre_archivo2]):
        if columna not in df.columns:
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' no existe")
            resultado = False
        elif not df[columna].apply(lambda x: len(str(x)) == longitud).all():
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' no tiene una longitud de {longitud} caracteres")
            resultado = False
        else:
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' superó la validación")
    return "\n".join(mensaje), resultado
# Regla: Verifica que una columna tenga la misma suma que en el otro archivo
def verifica_suma_columna(df1, df2, columna):
    mensaje = []
    resultado = True
    for df, nombre_archivo in zip([df1, df2], [nombre_archivo1, nombre_archivo2]):
        if columna not in df.columns:
            mensaje.append(f"En {nombre_archivo}, la columna '{columna}' no existe")
            resultado = False
    if resultado:
        suma1 = df1[columna].sum()
        suma2 = df2[columna].sum()
        if suma1 == suma2:
            mensaje.append(f"La suma de la columna '{columna}' es igual en ambos archivos: {suma1} y {suma2}")
        else:
            mensaje.append(f"La suma de la columna '{columna}' es diferente\nSuma en {nombre_archivo1}: {suma1}\nSuma en {nombre_archivo2}: {suma2}")
            resultado = False
    return "\n".join(mensaje), resultado

# Aplicar reglas
reglas = [
    ("verificar_nombre_columnas", verifica_nombre_columnas),
    ("verificar_cantidad_columnas", verifica_cantidad_columnas),
    ("verificar_cantidad_filas", verifica_cantidad_filas),
    ("verifica_columna_format_monto_Saldo_Capital", lambda df1, df2: verifica_columna_format_monto(df1, df2, 'Saldo_Capital')),
    ("verificar_columna_longitud_Rubro_GastoJudicial", lambda df1, df2: verifica_columna_longitud(df1, df2, 'Rubro_GastoJudicial', 13)),
    ("verifica_suma_columna_Saldo_Capital", lambda df1, df2: verifica_suma_columna(df1, df2, 'Saldo_Capital'))
]

for nombre_regla, regla in reglas:
    mensaje, exito = regla(df1, df2)
    mensaje_dividido = "\n".join(textwrap.wrap(mensaje, width=70))
    resultados.append([nombre_regla, mensaje_dividido, "Pasó" if exito else "Falló"])

# Mostrar resultados en una tabla
print(tabulate(resultados, headers=["Regla", "Resultado", "Estado"], tablefmt="pretty"))


#EJECUTA
#python verificar_csv.py