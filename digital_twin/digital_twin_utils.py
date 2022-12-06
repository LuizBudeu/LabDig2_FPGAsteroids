import csv

def get_integer_data_from_csv(filename: str) -> tuple[list[str], list[list[int]]]:

    rows = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if len(row) != 0:
                rows.append(row)

    column_row = rows[0]
    data_rows = [list(map(int, row)) for row in rows[1:]]

    return column_row, data_rows

def get_float_data_from_csv(filename: str) -> tuple[list[str], list[list[float]]]:

    rows = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if len(row) != 0:
                rows.append(row)

    column_row = rows[0]
    data_rows = [list(map(float, row)) for row in rows[1:]]

    return column_row, data_rows
