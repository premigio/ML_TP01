# Arbol de bayes
parents = {"rank": [], "gre": ["rank"], "gpa": ["rank"], "admit": ["rank", "gre", "gpa"]}  # relaciones de padres
values = {"admit": [0, 1], "gre": [0, 1], "gpa": [0, 1], "rank": [1, 2, 3, 4]}  # valores posibles de las variables
nodes = ["admit", "gre", "gpa", "rank"]  # nodos


# Normalizacion de la data
def getData():
    data = []
    with open('./resources/Admision.csv', 'r') as data_file:
        data_file.readline()
        for line in data_file:
            line = line.split(',')
            admit = int(line[0])
            gre = 1 if float(line[1]) >= 500 else 0
            gpa = 1 if float(line[2]) >= 3 else 0
            rank = int(line[3])
            data.append({"admit": admit, "gre": gre, "gpa": gpa, "rank": rank})
    return data


def product(*args):
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for product in result:
        yield tuple(product)


def permuteParentsValues(node):
    aux = {}
    for parent in parents[node]:
        aux[parent] = values[parent]
    return [tuple(v) for v in product(*aux.values())]


def getConditionalProbabilities(data):
    # inicializamos diccionarios de frecuencias
    frequencies_nominator = {}
    frequencies_denominator = {}
    for node in nodes:  # por cada nodo
        for val in values[node]:  # por cada variable del nodo
            tuple = (node, val)
            frequencies_nominator[tuple] = {}
            for combination in permuteParentsValues(node):  # padres **
                frequencies_nominator[tuple][combination] = 0
                frequencies_denominator[combination] = 0

    distinct_parents = []
    for vals in parents.values():
        if vals not in distinct_parents:
            distinct_parents.append(vals)

    # contabilizacion de frecuencias
    for row in data:
        for node_, parents_ in parents.items():
            tupleNode = (node_, row[node_])
            tupleParents = ()
            for parent in parents_:
                tupleParents = (*tupleParents, row[parent])
            frequencies_nominator[tupleNode][tupleParents] += 1
        for dparents in distinct_parents:
            tupleParents = ()
            for parent in dparents:
                tupleParents = (*tupleParents, row[parent])
            frequencies_denominator[tupleParents] += 1

    # probabilidades condicionales
    probabilities = {}
    for k in frequencies_nominator:
        probabilities[k] = {}
        for v in frequencies_nominator[k]:
            probabilities[k][v] = float(frequencies_nominator[k][v] + 1) / float(frequencies_denominator[v] + 1) # aplico laplace (esta bien hacerlo aca?)
    return probabilities


def probabilidadConjunta(conditionalProbabilities_, nodes_):
    aux = {}
    for node, vals in values.items():
        if node in nodes_:
            aux[node] = [nodes_[node]]
        else:
            aux[node] = vals
    aux = [dict(zip(aux, v)) for v in product(*aux.values())]
    ret = 0
    for d in aux:
        ret_aux = 1
        for node, value in d.items():
            tupleNode = (node, value)
            tupleParents = ()
            for parent in parents[node]:
                tupleParents = (*tupleParents, d[parent])
            ret_aux *= conditionalProbabilities_[tupleNode][tupleParents]
        ret += ret_aux
    return ret


def probabilidadCondicional(condProb ,prob, condition):
    return probabilidadConjunta(condProb, {**prob, **condition}) / probabilidadConjunta(condProb, condition)


print("4 a)")
print(probabilidadCondicional(getConditionalProbabilities(getData()), {"admit": 0}, {"rank": 1}))


print("4 b)")
print(probabilidadCondicional(getConditionalProbabilities(getData()), {"admit": 1}, {"rank": 2, "gre": 0, "gpa": 1}))
