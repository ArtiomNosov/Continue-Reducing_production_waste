import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast

df_from_csv = pd.read_csv("Experiments/out.csv", low_memory=False)

#Percent of biigests height
PERCENT = 5

def drop_negative_heights(file):
    indexes_to_drop = []
    for i in range(file.shape[0]):
        if file.iat[i, 0] < 0:
            indexes_to_drop.append(i)
    indexes_to_keep = set(range(file.shape[0])) - set(indexes_to_drop)
    file = file.take(list(indexes_to_keep))
    return file


def find_avg_height(dataframe: pd.DataFrame, percent):
    avg_height = 0
    series_heights = []
    count_lines = dataframe.shape[0]
    max_len_series = round(count_lines * (100 - percent) / 100)
    print(max_len_series)
    for i in range(dataframe.shape[0]):
        series_heights.append(dataframe.iat[i, 0])
    series_heights.sort()
    for i in range(max_len_series):
        series_heights.pop(0)
    for item in series_heights:
        avg_height += item
    avg_height = avg_height / len(series_heights)
    return avg_height



# Out plot: y - count of i-pos, x - shapes
def print_plot_for_position_75(dataframe: pd.DataFrame, position: int):
    global PERCENT
    groups = []
    counts = []
    count_colomns = len(dataframe.columns.tolist()) - 1
    count = 0
    avg = find_avg_height(df_from_csv, PERCENT)
    for i in range(dataframe.shape[0]):
        if dataframe.iat[i, 0] > avg:
            count += 1
            for j in range(1, count_colomns + 1):
                x = dataframe.iat[i, j]
                x = ast.literal_eval(x)
                if str(x) not in groups:
                    groups.append(str(x))
                    counts.append(0)

    for i in range(dataframe.shape[0]):
        if dataframe.iat[i, 0] > avg:
            print("Index: " + str(i))
            x = dataframe.iat[i, position]
            x = ast.literal_eval(x)
            index = groups.index(str(x))
            counts[index] += 1

    print(groups)
    print(counts)
    print(count)
    plt.bar(groups, counts)
    plt.show()

    return dataframe


# 1)Remove negative values of height (only for positive analysis!!!)
df_from_csv_1 = drop_negative_heights(df_from_csv)
for i in range(1, df_from_csv_1.shape[1]):
    print_plot_for_position_75(df_from_csv_1, i)
