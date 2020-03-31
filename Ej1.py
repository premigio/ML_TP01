def calculate_oyente(pref, probability_dic, listeners_proportion):
    final_p = {}

    for i in range(len(pref)):
        for j in probability_dic.keys():
            final_p[j] = final_p.get(j, listeners_proportion[j]) * (
                probability_dic[j][i] if pref[i] == 1 else 1 - probability_dic[j][i])

    oyente_final = max(final_p, key=final_p.get)

    return oyente_final, final_p


pgj = [0.95, 0.05, 0.02, 0.20]
pgv = [0.03, 0.82, 0.34, 0.92]

probabilities = {
    'joven': [0.95, 0.05, 0.02, 0.20],
    'viejo': [0.03, 0.82, 0.34, 0.92]
}

pv = 0.9

oyente = [1, 0, 1, 0]

oyente_str, probabilities = calculate_oyente(oyente, probabilities, {'joven': 1.0 - pv, 'viejo': pv})

print('La probabilidad que sea joven es ' + str(probabilities['joven']))
print('La probabilidad que sea viejo es ' + str(probabilities['viejo']))
print('El oyente es probablemente ' + oyente_str)
