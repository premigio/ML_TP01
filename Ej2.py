import pandas as pd
import BayesNaive as bayes_naive


def import_country_british(findout_country):
    file_xlsx = './resources/PreferenciasBritanicos.xlsx'

    data = pd.read_excel(file_xlsx, usecols='A:F', userows='2,14')

    bayes = bayes_naive.BayesNaive(['I', 'E'])

    all_prob = bayes.train(data, 5, -1)
    print(all_prob)
    # print(bayes.check(findout_country, all_prob,-1))


def analyse_country_likings(findout_country):
    global index
    df = open('./resources/PreferenciasBritanicos.csv', 'r')
    probability_per_country = [[0 for x in range(5)] for y in range(2)]
    total_probability = [0 for x in range(5)]
    indexes = [0 for x in range(2)]
    index = 0
    for preference_vectors_aux in df.readlines():
        if index > 0:
            preference_vectors = preference_vectors_aux.split(';')
            if preference_vectors[5] == 'I\r\n' or preference_vectors[5] == 'I':
                country = 0
                indexes[0] += 1
            else:
                country = 1
                indexes[1] += 1
            for i in range(0, 5):
                probability_per_country[country][i] += int(preference_vectors[i])
                total_probability[i] += int(preference_vectors[i])
        index += 1
    #print(probability_per_country)

    for i in range(0, 5):
        probability_per_country[0][i] += 1
        probability_per_country[0][i] /= float(indexes[0] + 2)
        probability_per_country[1][i] += 1
        probability_per_country[1][i] /= float(indexes[1] + 2)
        total_probability[i] /= float(index - 1)
    #print(probability_per_country)

    max_prob = 0.0
    max_country = 'No country'
    for i in range(0, 2):
        given_probability = 1.0
        for j in range(0, 5):
            if findout_country[j] != 0:
                given_probability *= probability_per_country[i][j]
            else:
                given_probability *= 1.0 - probability_per_country[i][j]

        country_prob = float(given_probability) * indexes[i] / index
        # me acelere el paso, despues meter mano aca
        max_prob = country_prob if max_prob < country_prob else max_prob
        max_country = 'Escoces' if max_prob <= country_prob and i == 1 else max_country
        max_country = 'Ingles' if max_prob <= country_prob and i == 0 else max_country
    return max_country, {'Ingles': probability_per_country[0], 'Escoces': probability_per_country[1]}

    # hasta aca tengo todas las probabilidades


findout = [1, 0, 1, 1, 0]
max_country_str, prob = analyse_country_likings(findout)
print('la persona es probablemente ' + max_country_str)
print(prob)

# print(import_country_british(findout))
