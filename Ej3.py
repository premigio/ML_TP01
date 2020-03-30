import pandas as pd
import random
import BayesNaive


# def to_int_matrix(noticias, index, text):
#     array = set()
#     for noticia in noticias:
#         if text:
#             for word in noticia[index].split():
#                 array.add(word)
#         else:
#             array.add(noticia[index])
#
#     array = list(array)
#
#     matrix = [[0 for j in range(len(array))] for k in range(len(noticias))]
#
#     for noticia in noticias:
#         if text:
#             for word in noticia[index].split():
#                 matrix[noticias.index(noticia)][array.index(word)] += 1
#         else:
#             matrix[noticias.index(noticia)][array.index(noticia[index])] += 1
#     return matrix


categories = ["Nacional", "Destacadas", "Deportes", "Salud", "Ciencia y Tecnologia", "Entretenimiento", "Economia",
              "Noticias destacadas", "Internacional"]
categories_to_delete = ["Nacional", "Salud", "Ciencia y Tecnologia", "Noticias destacadas", "Internacional"]
categories_to_train = ["Destacadas", "Deportes", "Entretenimiento", "Economia"]

file_xlsx = './resources/Noticias_argentinas.xlsx'

data_frame = pd.read_excel(file_xlsx, usecols='A:D').drop_duplicates()

for i in range(0, len(categories_to_delete)):
    data_frame = data_frame[data_frame['categoria'] != categories_to_delete[i]]

column_names = data_frame.columns.values
noticias = data_frame.values.tolist()

random.shuffle(noticias)
quarter = len(noticias) // 4  # Floor division
noticias = noticias[:quarter]
noticias_aux = list()
for i in range(len(noticias)):
    noticias_aux.append(noticias[i][1:])

bayes = BayesNaive.BayesNaive(categories_to_train)
category_prob = bayes.train(noticias_aux, 2, 0)

print(bayes.check(['Alquileres congelados: inmobiliarias e inquilinos están de acuerdo con la medida y creen que se '
                   'contemplaron los motivos de conflicto', 'Infobae.com'], category_prob, 0))

# word_count_matrix = to_int_matrix(noticias, 1, True)
