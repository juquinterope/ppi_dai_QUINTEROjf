import pandas as pd

df = pd.read_csv('../data/municipios.csv')
print(df.head())

# print(df.isnull().count())
print(df.columns)
columns = ['Nombre Municipio', 'Tipo Centro Poblado', 'Longitud', 'Latitud']
df = df[columns]

# En el dataframe, esta presente no solo el municipio sino tambien
# todas sus divisiones como: corregimientos o barrios;
# se tomara en cuenta unicamente el centro del municipio que hace
# referencia a su 'CABECERA MUNICIPAL'
df = df[df['Tipo Centro Poblado'] == 'CABECERA MUNICIPAL']
# Posteriormente la columna no es util
df = df[['Nombre Municipio', 'Longitud', 'Latitud']]
print(df.head())
df.to_csv('../data/municipios_filtrados.csv', index=False)
