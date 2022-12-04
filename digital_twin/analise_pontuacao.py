# tempo nos modos de jogo em uma sessão: modo de jogo mais divertido/chato
# tempo de desviar do asteroide: tempo de reação
# pontuação em cada modo: dificuldade de cada modo

import csv
import matplotlib.pyplot as plt

rows = []

with open('pontuacao.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        # print(', '.join(row))
        if len(row) != 0:
            rows.append(row)

column_row = rows[0]
data_rows = [list(map(int, row)) for row in rows[1:]]

plt.plot([data_row[0] for data_row in data_rows], [data_row[1] for data_row in data_rows], 'ro')
plt.xlabel(column_row[0])
plt.ylabel(column_row[1])
plt.show()