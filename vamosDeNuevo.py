parents = {"rank": [], "gre": ["rank"], "gpa": ["rank"], "admit": ["rank", "gre", "gpa"]}  # relaciones de padres
values = {"admit": [0, 1], "gre": [0, 1], "gpa": [0, 1], "rank": [1, 2, 3, 4]}  # valores posibles de las variables
nodes = ["admit", "gre", "gpa", "rank"]  # nodos


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


def conditionalProbabilities(data):
    # inicializamos diccionarios de frecuencias
    frequencies_nominator = {}
    frequencies_denominator = {}
    for node in nodes:  # por cada nodo
        frequencies_denominator[node] = {}
        for val in values[node]:  # por cada variable del nodo
            tuple = (node, val)
            frequencies_nominator[tuple] = {}
            for combination in permuteParentsValues(node):
                frequencies_nominator[tuple][combination] = 0
                frequencies_denominator[node][combination] = 0

    for row in data:
        for node_, parents_ in parents.items():
            tupleNode = (node_, row[node_])
            tupleParents = ()
            for parent in parents_:
                tupleParents = (*tupleParents, row[parent])
            frequencies_nominator[tupleNode][tupleParents] += 1
            frequencies_denominator[node_][tupleParents] += 1

    probabilities = {}
    for k in frequencies_nominator:
        probabilities[k] = {}
        for v in frequencies_nominator[k]:
            probabilities[k][v] = float(frequencies_nominator[k][v] + 1) / float(frequencies_denominator[k[0]][v] + 1)

    return probabilities


def ej2():
    probabilities = conditionalProbabilities(getData())
    print(probabilities)
    prob = {"admit": 1}
    condition = {"rank": 2, "gre": 0, "gpa": 1}
    ret = 1
    joint = {**prob, ** condition}
    for node, value in joint.items():
        tupleNode = (node, value)
        tupleParents = ()
        for parent in parents[tupleNode[0]]:
            tupleParents = (*tupleParents, joint[parent])
        ret *= probabilities[tupleNode][tupleParents]


    return ret



def calculate(condProb ,prob, condition):
    if len(prob) == 0:
        return 1

    probabilities = condProb
    tupleNode = (list(prob.keys())[0], prob[list(prob.keys())[0]])
    joint = {**prob, **condition}
    ret = 1

    for node, value in joint.items():
        aux = {}
        tupleNode = (node, value)
        for parent in parents[tupleNode[0]]:
            if parent in joint:
                aux[parent] = []
                aux[parent].append(joint[parent])
            else:  # calculamos probabilidad total
                aux[parent] = values[parent]
        tupleParents = [tuple(v) for v in product(*aux.values())]
        total_prob = 0
        for tp in tupleParents:
            total_prob += probabilities[tupleNode][tp]
        ret *= total_prob

    return ret / calculate(probabilities,condition, {})

print(ej2())
print(calculate(conditionalProbabilities(getData()), {"admit": 1}, { "rank": 2, "gre": 0, "gpa": 1}))
# print(calculate(conditionalProbabilities(getData()), {"admit": 0}, {"rank": 1}))