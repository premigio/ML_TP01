import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import random
import BayesNaive


# calculo de la matriz de confusion
def confusion_matrix(test_noticias, probabilities, train_categories, this_bayes):
    results = {}

    total = 0
    for noticia in test_noticias:
        if noticia[2] in train_categories:
            result, prob = this_bayes.check([noticia[0], noticia[1]], probabilities, 0)
            results[noticia[2]] = results.get(noticia[2], {})
            results[noticia[2]][result] = results[noticia[2]].get(result, 0) + 1
            total += 1
    return results, total


def get_true_false_results(categories_to_train, classification_results):
    true_positive = {}
    false_positive = {}
    true_negative = {}
    false_negative = {}
    for cat in categories_to_train:
        for i in classification_results.keys():
            for j in classification_results.keys():
                if classification_results[i].get(j, 0) == 0:
                    classification_results[i][j] = 0
                if i == cat:
                    if i == j:
                        true_positive[cat] = true_positive.get(cat, 0) + classification_results[i][j]
                    else:
                        false_negative[cat] = false_negative.get(cat, 0) + classification_results[i][j]
                elif j == cat:
                    false_positive[cat] = false_positive.get(cat, 0) + classification_results[i][j]
                else:
                    true_negative[cat] = true_negative.get(cat, 0) + classification_results[i][j]
    return true_positive, false_positive, true_negative, false_negative


def prepare_roc_points(noticias_data, categories):
    tasa_vp_array = []
    tasa_fp_array = []
    tasa_roc_array = []

    division_options = [len(noticias_data) // x for x in range(2, 5)]
    division_options.append(40)
    division_options.append(int(3/4 * len(noticias_data)))
    graph_values = {}
    for amount_now in division_options:
        random.shuffle(noticias_data)

        aux_set = list()
        for no in range(len(noticias_data)):
            aux_set.append(noticias_data[no][1:])

        train_set = aux_set[:amount_now]
        test_set = aux_set[amount_now:]

        new_bayes = BayesNaive.BayesNaive(categories)
        category_proba = new_bayes.train(train_set, 2, 0)

        results, total_results = confusion_matrix(test_set, category_proba, categories, new_bayes)
        tp, fp, tn, fn = get_true_false_results(categories, results)
        for key in categories:
            graph_values[key] = graph_values.get(key, {})
            graph_values[key]['x'] = graph_values[key].get('x', [])
            graph_values[key]['x'].append(fp[key] / (fp[key] + tn[key]))
            graph_values[key]['y'] = graph_values[key].get('y', [])
            graph_values[key]['y'].append(tp[key] / (tp[key] + fn[key]))
            tasa_roc_array.append({i: [fp[i] / (fp[i] + tn[i]), tp[i] / (tp[i] + fn[i])] for i in categories})
    for key in categories:
        xs, ys = zip(*sorted(zip(graph_values[key]['x'], graph_values[key]['y'])))
        plt.plot(xs, ys)
    plt.ylabel("Tasa verdadero positivo")
    plt.xlabel("Tasa falso positivo")
    plt.title("ROC curve")
    plt.show()


    

categories = ["Nacional", "Destacadas", "Deportes", "Salud", "Ciencia y Tecnologia", "Entretenimiento", "Economia",
              "Noticias destacadas", "Internacional"]
categories_to_delete = ["Nacional", "Ciencia y Tecnologia", "Noticias destacadas", "Destacadas", "Salud"]
categories_to_train = ["Internacional", "Deportes", "Entretenimiento", "Economia"]

file_xlsx = './resources/Noticias_argentinas.xlsx'

data_frame = pd.read_excel(file_xlsx, usecols='A:D').drop_duplicates()

for i in range(0, len(categories_to_delete)):
    data_frame = data_frame[data_frame['categoria'] != categories_to_delete[i]]

column_names = data_frame.columns.values
noticias = data_frame.values.tolist()

random.shuffle(noticias)
quarter = 3 * len(noticias) // 4  # Floor division

noticias_aux = list()

for i in range(len(noticias)):
    noticias_aux.append(noticias[i][1:])

noticias_train = noticias_aux[:quarter]
noticias_test = noticias_aux[quarter:]

bayes = BayesNaive.BayesNaive(categories_to_train)
category_prob = bayes.train(noticias_train, 2, 0)

classification_results, total = confusion_matrix(noticias_test, category_prob, categories_to_train, bayes)


m_confussion = [[0.0 for i in range(0, len(classification_results.keys()))] for j in range(0, len(classification_results.keys()))]
print(classification_results)
i = 0
for key in sorted(classification_results.keys()):
    values = classification_results[key]
    j = 0
    for k in sorted(classification_results.keys()):
        m_confussion[i][j]= values[k]
        j += 1
    i += 1

df_cm = pd.DataFrame(m_confussion, index = [i for i in sorted(classification_results.keys())],
                  columns = [i for i in sorted(classification_results.keys())])
plt.figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True,  fmt='g')
plt.show()


tp, fp, tn, fn = get_true_false_results(categories_to_train, classification_results)

# calculo de precision, accuracy, tasa de v positivos, de f positivos y F1-score

accuracy = {i: (tp[i] + tn[i]) / (tp[i] + tn[i] + fp[i] + fn[i]) for i in categories_to_train}
precision = {i: tp[i] / (tp[i] + fp[i]) for i in categories_to_train}
recall = {i: tp[i] / (tp[i] + fn[i]) for i in categories_to_train}
f1score = {i: 2 * precision[i] * recall[i] / (precision[i] + recall[i]) for i in categories_to_train}
tasa_vp = {i: tp[i] / (tp[i] + fn[i]) for i in categories_to_train}
tasa_fp = {i: fp[i] / (fp[i] + tn[i]) for i in categories_to_train}

prepare_roc_points(noticias, categories_to_train)


# print(accuracy)
# print(precision)
# print(recall)
# print(f1score)
# print(tasa_vp)
# print(tasa_fp)
