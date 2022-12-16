# Cada linha da tabela tempo_de_jogo.csv significa o tempo total gasto pelo jogador
# em cada um dos modos em uma sessão de jogo

# Interpretação: popularidade ou nível de entretenimento de cada modo

from digital_twin_utils import get_float_data_from_csv
import matplotlib.pyplot as plt

column_row, data_rows = get_float_data_from_csv("tempo_de_jogo.csv")

tempo_total_modo1 = sum([data_row[0] for data_row in data_rows])
tempo_total_modo2 = sum([data_row[1] for data_row in data_rows])
tempo_total_modo3 = sum([data_row[2] for data_row in data_rows])
tempo_total_modo4 = sum([data_row[3] for data_row in data_rows])

names = column_row
values = [tempo_total_modo1, tempo_total_modo2, tempo_total_modo3, tempo_total_modo4]

plt.title("Tempo acumulado por modo de jogo")
plt.xlabel("Modo de jogo")
plt.ylabel("Tempo acumulado (s)")
plt.bar(names, values)
plt.show()