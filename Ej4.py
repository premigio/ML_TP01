import BayesNaive


def import_data():
    # retorna los datos pero con la data discretizada en un array
    df = open('./resources/Admision.csv', 'r')

    index = 0
    aux = df.readlines()
    data = [[] for i in range(len(aux) - 1)]  # me armo la lista como deberia tener para bayes
    for admission_line in aux:
        line = admission_line.split(',')
        if index:
            data[index - 1] = [None for i in range(len(line))]
            for i in range(len(line)):
                if i == 0 or i == 3:  # case admit | rank
                    data[index - 1][i] = int(line[i])
                if i == 1:  # case gre
                    data[index - 1][i] = 'gre_above' if float(line[i]) >= 500 else 'gre_below'
                if i == 2:  # case gpa
                    data[index - 1][i] = 'gpa_above' if float(line[i]) >= 3 else 'gpa_below'
        index += 1
    return data, index - 1


def calculate_probability_table(data, node, parents):
    # nodo es la columna en data que representa al gpa, gre, rank, admit
    # Parents un dict de cuales son los padres para ver la relacion y cuales son las posibles cosas
    # retorno la diccionario de probabilidades equivalente a todos los P(nodo = x | parentA = a, parentB = b ... ) para todos x,a,b, etc en su dominio
    aux = [len(x) for x in parents.values()]
    possibilities = 1
    for i in aux:
        possibilities *= i
    parent_array = {}
    index_array = {}

    for i in range(len(data)):
        aux = []
        for j in parents.keys():
            aux.append(data[i][j])
        p_tuple = tuple(aux)
        parent_array[p_tuple] = parent_array.get(p_tuple, {data[i][node]: 0.0})
        parent_array[p_tuple][data[i][node]] = parent_array[p_tuple].get(data[i][node], 0.0) + 1.0
        index_array[p_tuple] = index_array.get(p_tuple, 0) + 1

    for tupl in parent_array.keys():
        for key in parent_array[tupl].keys():
            parent_array[tupl][key] /= float(index_array[tupl])
        if not any(parents):
            return parent_array[tupl]
    return parent_array


admission_data, data_amount = import_data()

admit_table = calculate_probability_table(admission_data, 0,
                                          {
                                              1: ['gre_above', 'gre_below'],
                                              2: ['gpa_above', 'gpa_below'],
                                              3: [1, 2, 3, 4]
                                          })  # P(admit | gre,gpa,rank)

gre_table = calculate_probability_table(admission_data, 1, {3: [1, 2, 3, 4]})  # P(gre | rank)
gpa_table = calculate_probability_table(admission_data, 2, {3: [1, 2, 3, 4]})  # P(gpa | rank)
rank_table = calculate_probability_table(admission_data, 3, {})  # P(rank)
admit_prob_table = calculate_probability_table(admission_data, 0, {}) # P(admit)
print(admit_table)
print(admit_prob_table)
# a) P(admit = 0 | rank = 1)
print(admit_table[tuple(['gre_below', 'gpa_above', 2])].get(0, 0.0)) #tamal

# b) P(admit = 1 | rank = 2, GPA = 3.5, GRE = 450) esta bien que de 0 ?
# print(admit_table[tuple(['gre_below', 'gpa_above', 2])].get(1, 0.0) * )

# falta el c) creo que es aprendizaje parametrico pues ya nos dan la estructura, pero anda a saber
