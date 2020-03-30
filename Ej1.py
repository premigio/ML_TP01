pgj = [0.95, 0.05, 0.02, 0.20]
pgv = [0.03, 0.82, 0.34, 0.92]

pv = 0.9

oyente = [1, 0, 1, 0]

p_oyente_joven = (1 - pv)
p_oyente_viejo = pv

for i in range(len(oyente)):
    p_oyente_joven *= pgj[i] if oyente[i] == 1 else 1 - pgj[i]
    p_oyente_viejo *= pgv[i] if oyente[i] == 1 else 1 - pgv[i]

print('La probabilidad que sea joven es ' + str(p_oyente_joven))
print('La probabilidad que sea viejo es ' + str(p_oyente_viejo))
oyente_str = 'viejo' if p_oyente_viejo > p_oyente_joven else 'joven'
print('El oyente es probablemente ' + oyente_str)
