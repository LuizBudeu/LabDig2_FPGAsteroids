from digital_twin_utils import get_float_data_from_csv
import matplotlib.pyplot as plt

column_row, data_rows = get_float_data_from_csv("tempo_de_jogo.csv")

plt.plot([data_row[0] for data_row in data_rows], [data_row[1] for data_row in data_rows], 'ro')
plt.xlabel(column_row[0])
plt.ylabel(column_row[1])
plt.show()