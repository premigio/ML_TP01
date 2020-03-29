from math import isnan


class BayesNaive:

    def __init__(self, categories):
        self.categories = categories
        self.indexes = [0 for x in range(len(categories))]
        self.index = 0
        self.word_array = [{} for x in range(len(categories))]
        self.word_index_count = [0 for x in range(len(categories))]

    def train(self, training_set, category_index, text_index):
        # seteo text_index a -1 para que no haya analisis de texto, sino hago el analisis palabra a palabra

        probability_per_category = [{} for y in range(len(self.categories))]
        for line in training_set:
            category = line[category_index]
            if isinstance(category, str) or not isnan(category):
                cat = self.categories.index(category)
                self.indexes[cat] += 1  # en cada categoria, busco la cantidad de veces que la tengo
                for i in range(len(line) - 1):
                    if i != text_index:
                        probability_per_category[cat][i] = probability_per_category[cat].get(i, {})
                        probability_per_category[cat][i][line[i]] = probability_per_category[cat][i].get(line[i], 0) + 1
                        # sumo para cada respectivo valor, las chances de cada item. ej= en categoria,
                        # deberia sumar para cada una el numero de veces que la tengo
                    else:
                        # analisis palabra por palabra
                        words = line[i].split()  # separo en un array de palabras
                        for word in words:
                            self.word_array[cat][word] = self.word_array[cat].get(word, 0) + 1
                            self.word_index_count[cat] += 1

                self.index += 1  # numero total de data

        for j in range(len(self.categories)):  # con correccion de laplace
            for i in probability_per_category[j].keys():
                for key in probability_per_category[j][i].keys():
                    probability_per_category[j][i][key] += 1
                    probability_per_category[j][i][key] /= float(self.indexes[j]
                                                                 + len(probability_per_category[j][i].keys()))
        for cat in range(len(self.categories)):
            for key in self.word_array[cat].keys():
                self.word_array[cat][key] += 1
                self.word_array[cat][key] /= float(self.word_index_count[cat] + len(self.word_array[cat]))
        print(probability_per_category)
        return probability_per_category

    def check(self, find_out, probability_per_category, text_index):
        max_prob = 0.0
        final_classification = 'None of the options'  # si termino con eso, manquie en algun lado
        for i in range(len(self.categories)):
            given_probability = 1.0
            for j in range(len(find_out) - 1):
                if j != text_index:
                    given_probability *= probability_per_category[i][j][find_out[j]]  # P(D|h)
                else:  # calculo la probabilidad de las palabras en el coso
                    words = find_out[j].split()
                    for word in words:
                        if word in self.word_array[i]:
                            word_prob = self.word_array[i][word]
                            given_probability *= word_prob
                        else:
                            # laplace para  count 0
                            given_probability *= 1 / (self.word_index_count[i] + len(self.word_array[i]))

            class_prob = self.indexes[i] / self.index  # probabilidad de la clasificacion P(h)
            classification_probability = float(given_probability) * class_prob
            print(classification_probability)
            # me acelere el paso, despues meter mano aca. wtf?? no me acuerdo mas de este comment
            max_prob = classification_probability if max_prob < classification_probability else max_prob
            final_classification = self.categories[
                i] if max_prob <= classification_probability else final_classification

        return final_classification, max_prob
