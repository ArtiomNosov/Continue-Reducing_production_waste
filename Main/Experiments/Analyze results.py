import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast
import Box2D_test as emulator
import Dataset.ListsWithDetailsCoordinates as dataset

# Percent of biggest heights
PERCENT = 4


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
    for i in range(dataframe.shape[0]):
        series_heights.append(dataframe.iat[i, 0])
    series_heights.sort()
    for j in range(max_len_series):
        series_heights.pop(0)
    return series_heights[0]


def find_used_area_percent(dataframe: pd.DataFrame):
    count_line = dataframe.shape[0]
    series_height = []
    shapes_area = []
    for i in range(count_line):
        series_height.append(dataframe.iat[i, 0])
    max_height = max(series_height)
    used_area = 0
    for j in range(dataframe.shape[1] - 1):
        shapes_area.append(int(dataframe.iat[1, j + 1].split(",")[0][1::]))
        used_area += int(dataframe.iat[1, j + 1].split(",")[0][1::])
    area = (emulator.HEIGHT - max_height) * emulator.LENGTH
    print(used_area / area * 100)


# Out plot: y - count of i-pos, x - shapes
def print_plot_for_position(dataframe: pd.DataFrame, position: int, filepath: str):
    global PERCENT
    groups = []
    counts = []
    count_columns = len(dataframe.columns.tolist()) - 1
    count = 0
    avg = find_avg_height(dataframe, PERCENT)

    for i in range(dataframe.shape[0]):
        if dataframe.iat[i, 0] >= avg:
            count += 1
            for j in range(1, count_columns + 1):
                x = dataframe.iat[i, j]
                x = ast.literal_eval(x)
                if str(x) not in groups:
                    groups.append(str(x))
                    counts.append(0)

    max_count = 0
    shape_with_max_count = ''
    for j in range(dataframe.shape[0]):
        if dataframe.iat[j, 0] >= avg:
            x = dataframe.iat[j, position]
            x = ast.literal_eval(x)
            index = groups.index(str(x))
            counts[index] += 1

    for k in range(len(counts)):
        if max_count < counts[k]:
            max_count = counts[k]
            shape_with_max_count = [groups[k].split(',')[2][2:-2:], groups[k].split(',')[0][1::]]

    plt.figure(figsize=(25, 7))
    plt.bar(groups, counts)

    plt.title("Position" + str(position))
    plt.savefig(f'{filepath}/Position {position}')
    plt.close()
    return shape_with_max_count


def plot_on_list(list: list):
    x = []
    y = []
    for item in list:
        x.append(item[0])
        y.append(item[1])
    plt.plot(x, y)
    plt.show()


# Док-во равновероятного распределения 76-83%
def stats_for_graph1(list_in: list, res_list: list):
    if not res_list:
        res_list = [[], [], [], [], [], [], []]
    for item in list_in:
        if 76 < item[1] < 77:
            res_list[0].append(item[0])
        if 77 < item[1] < 78:
            res_list[1].append(item[0])
        if 78 < item[1] < 79:
            res_list[2].append(item[0])
        if 79 < item[1] < 80:
            res_list[3].append(item[0])
        if 80 < item[1] < 81:
            res_list[4].append(item[0])
        if 81 < item[1] < 82:
            res_list[5].append(item[0])
        if 82 < item[1] < 83:
            res_list[6].append(item[0])
    return res_list


# Средний номер 1го лучшего процента 76-83%
def stats_for_graph2(list_in: list, res_list: list):
    if not res_list:
        res_list = [[], [], [], [], [], [], []]
    for item in list_in:
        if 76 < item[1] < 77 and res_list[0] == []:
            res_list[0].append(item[0])
        if 77 < item[1] < 78 and res_list[1] == []:
            res_list[1].append(item[0])
        if 78 < item[1] < 79 and res_list[2] == []:
            res_list[2].append(item[0])
        if 79 < item[1] < 80 and res_list[3] == []:
            res_list[3].append(item[0])
        if 80 < item[1] < 81 and res_list[4] == []:
            res_list[4].append(item[0])
        if 81 < item[1] < 82 and res_list[5] == []:
            res_list[5].append(item[0])
        if 82 < item[1] < 83 and res_list[6] == []:
            res_list[6].append(item[0])
    return res_list


def calculate_for_stats(res_list):
    for i in range(len(res_list)):
        ids = 0
        for j in range(len(res_list[i])):
            ids += res_list[i][j]
        if len(res_list[i]) != 0:
            res_list[i] = ids / len(res_list[i])
    return res_list

#df_from_csv = pd.read_csv("Experiments/Results/EXP4/out.csv", low_memory=False)

# 1)Remove negative values of height (only for positive analysis!!!)
#df_from_csv_1 = drop_negative_heights(df_from_csv)


s1 = [dataset.У80_У511_скос_1, 4, "У80_У511_скос_1"]
s2 = [dataset.У80_У509_1, 4, "У80_У509_1"]
s3 = [dataset.Л10_У689, 4, "Л10_У689"]
s4 = [dataset.Л10_У688, 4, "Л10_У688"]
s5 = [dataset.Л10_У531, 4, "Л10_У531"]
s6 = [dataset.Л10_У530, 4, "Л10_У530"]
s7 = [dataset.Л10_У528, 4, "Л10_У528"]
s8 = [dataset.Л10_У527_гиб_1, 4, "Л10_У527_гиб_1"]
s9 = [dataset.Л10_У526_гиб_1, 4, "Л10_У526_гиб_1"]
s10 = [dataset.Л10_У525_гиб_1, 4, "Л10_У525_гиб_1"]
s11 = [dataset.Л10_У523_гиб_1, 4, "Л10_У523_гиб_1"]
s12 = [dataset.Л10_У521_1_гиб_1, 4, "Л10_У521_1_гиб_1"]
s13 = [dataset.У90_У503А_скос_1, 4, "_СБ_У533_1"]
s14 = [dataset.У80_У534_гиб_1, 4, "У80_У534_гиб_1"]
FIGURES_LIST = [s1, s2, s3, s4, s5, s6, s7, s8]
res_list = []

results = emulator.get_best_position(FIGURES_LIST, max_time=100000)
graph_param = results[2]
#print(graph_param)
graph_param.pop(0)
#plot_on_list(graph_param)
res_list = stats_for_graph2(graph_param, res_list)

results = emulator.get_best_position(FIGURES_LIST, max_time=100000)
graph_param = results[2]
#print(graph_param)
graph_param.pop(0)
#plot_on_list(graph_param)
res_list = stats_for_graph2(graph_param, res_list)

results = emulator.get_best_position(FIGURES_LIST, max_time=100000)
graph_param = results[2]
#print(graph_param)
graph_param.pop(0)
#plot_on_list(graph_param)
res_list = stats_for_graph2(graph_param, res_list)

res_list = calculate_for_stats(res_list)
print(res_list)

'''
df_from_csv = pd.read_csv("Experiments/Results/EXP1/out.csv", low_memory=False)
df_from_csv_1 = drop_negative_heights(df_from_csv)
for i in range(1, df_from_csv_1.shape[1]):
  shape = print_plot_for_position(df_from_csv_1, i, 'Experiments/Results/EXP1')
  print(f"Position: {i}, shape: {shape}")

print("===========================")

df_from_csv = pd.read_csv("Experiments/Results/EXP2/out.csv", low_memory=False)
df_from_csv_1 = drop_negative_heights(df_from_csv)
for i in range(1, df_from_csv_1.shape[1]):
    shape = print_plot_for_position(df_from_csv_1, i, 'Experiments/Results/EXP2')
    print(f"Position: {i}, shape: {shape}")

print("===========================")

df_from_csv = pd.read_csv("Experiments/Results/EXP3/out.csv", low_memory=False)
df_from_csv_1 = drop_negative_heights(df_from_csv)
for i in range(1, df_from_csv_1.shape[1]):
    shape = print_plot_for_position(df_from_csv_1, i, 'Experiments/Results/EXP3')
    print(f"Position: {i}, shape: {shape}")

print("===========================")

df_from_csv = pd.read_csv("Experiments/Results/EXP4/out.csv", low_memory=False)
df_from_csv_1 = drop_negative_heights(df_from_csv)
for i in range(1, df_from_csv_1.shape[1]):
    shape = print_plot_for_position(df_from_csv_1, i, 'Experiments/Results/EXP4')
    print(f"Position: {i}, shape: {shape}")
'''
