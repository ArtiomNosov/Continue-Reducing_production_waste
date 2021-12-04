import Box2D_test as emulator
import time
import Dataset.ListsWithDetailsCoordinates as dataset

# TODO: Do all iterations with 10! combinations (permutations). Create picture with coordinates (count iterations, percent of used area)
# TODO: Do all iterations with 15! combinations (permutations). Create picture with coordinates (count iterations, percent of used area)

# Эксперимент с разными конфигурациями бросания фигур
#
# [size (polygon), type]
# Type of drawing figures: 1 - circles, 2 - triangle, 3 - squares, 4 - polygon
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
start_time1 = time.time()


#emulator.create_csv_of_experiment(FIGURES_LIST, "out.csv")

results = emulator.get_best_position(FIGURES_LIST, max_time=10)
print(str(results[0]))
for item in results[1]:
    print(item)

graph_param = results[2]


print("---RESULT TIME IS %s SECONDS ---" % (time.time() - start_time1))
