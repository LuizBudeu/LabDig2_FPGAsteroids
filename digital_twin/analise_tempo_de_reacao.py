# Cada linha de tempo_de_reacao.csv representa o tempo entre
# o asteroide cruzar a linha amarela e a nave desviar

# Interpretação: é possível inferir o quão lento é o agente
# controlador da nave em cada modo de jogo

from digital_twin_utils import get_float_data_from_csv
import matplotlib.pyplot as plt

column_row, data_rows = get_float_data_from_csv("tempo_de_reacao.csv")

plt.title("Gráfico de dispersão tempo de reação X Modo de jogo")
plt.xlabel("Modo de jogo")
plt.ylabel("Tempo de reação")
plt.plot([data_row[0] for data_row in data_rows], [data_row[1] for data_row in data_rows], 'ro')
plt.show()