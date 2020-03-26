import pandas as pd
import random

categories = ["Nacional", "Destacadas", "Deportes", "Salud", "Ciencia y Tecnologia", "Entretenimiento", "Economia",
              "Noticias destacadas"]
categories_to_delete = ["Nacional", "Salud", "Ciencia y Tecnologia", "Noticias destacadas"]

file_xlsx = './resources/Noticias_argentinas.xlsx'

data_frame = pd.read_excel(file_xlsx, usecols='A:D')

for i in range(0, len(categories_to_delete)):
    data_frame = data_frame[data_frame['categoria'] != categories_to_delete[i]]

column_names = data_frame.columns.values
noticias = data_frame.values.tolist()

random.shuffle(noticias)
half = len(noticias) // 2  # Floor division
noticias = noticias[:half]
