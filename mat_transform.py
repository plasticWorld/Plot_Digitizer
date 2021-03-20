import numpy as np
import os, cv2, json
import matplotlib.pyplot as plt


def draw_plot(lineCoordinates, lineParam):
    # set plot view
    plt.plot(lineCoordinates.keys(), lineCoordinates.values(), label=lineParam, linewidth=1)
    if float(width_dim_begin) >= float(width_dim):
        x2 = float(width_dim_begin)
        x1 = float(width_dim)
    else:
        x1 = float(width_dim_begin)
        x2 = float(width_dim)

    if float(height_dim_begin) >= float(height_dim):
        y2 = float(height_dim_begin)
        y1 = float(height_dim)
    else:
        y1 = float(height_dim_begin)
        y2 = float(height_dim)

    plt.axis([x1, x2, y1, y2])
    # plt.gca().invert_yaxis()
    plt.grid(True)


def load_list(folder):
    # получение списка файлов
    files = os.listdir(folderToFindImg)
    # определение шаблона
    names = filter(lambda x: x.endswith('.png'), files)
    return names


def transform_coordinates(space, tempMatrix, widthDelta, heightDelta, xMin, yMin):
    # получаем 2 списока индексов не нулевых элементов
    # номер строки и номер столбца
    tempY, tempX = np.nonzero(tempMatrix)

    # getting plot scale coef by axis
    ratioScaleX = round((widthDelta / tempMatrix.shape[1]), 10)
    ratioScaleY = round((heightDelta / len(tempMatrix)), 10)

    # getting real plot coordinates of x and y
    # xMin, yMin - сдвиг по осям по начальной точке(минимальным значениям)
    tempX = (tempX * ratioScaleX + float(xMin)).round(5)
    tempY = (tempY * ratioScaleY + float(yMin)).round(5)
    # add to temp dict structure x as key and y as value
    tempDict = dict(zip(tempX[0::space], tempY[0::space]))
    return tempDict


width_dim_begin, height_dim_begin = (input("Input min initial of axes (1)wigth, (2)height (default: 0 0)\n"
                                           "Введите минимальные значения сетки графика через пробел: ") or "0 0").split()

width_dim, height_dim = (input("Input max final values of axes (1)wigth, (2)height (default: 1 1)\n"
                               "Введите максимальные значения сетки графика через пробел: ") or "1 1").split()

space = int(input("Input space value (default: 10%)\n"
                  "Введите процент разреживания(каждый КАКОЙ столбец учитывается): ") or "20")

# round float to 2 digits after dot
widthDelta = round((float(width_dim) - float(width_dim_begin)), 2)
heightDelta = round((float(height_dim) - float(height_dim_begin)), 2)

# определение пути
folderToFindImg = 'res/skeleton/'
filesNames = load_list(folderToFindImg)

# словарь словарей координат - внешний ключ - параметр кривой, внутренний - координата Х
plotsDict = {}

for currentFile in filesNames:
    tempMatrix = cv2.imread(folderToFindImg + currentFile, 0)  # 0 - for gray color scheme:(0, 255)
    # отражаем матрицу, чтобы соориентировать ось у по направлению увеличения индексов строк
    tempMatrix = cv2.flip(tempMatrix, 0)
    # percent of sparseness
    space = int(len(tempMatrix[0]) / (tempMatrix.shape[1] * (space / 100)))
    tempDict = transform_coordinates(space, tempMatrix, widthDelta, heightDelta, width_dim_begin, height_dim_begin)
    # add dict of plot coordinates to final dict with curve name(digital) as key
    plotsDict[currentFile[:-4]] = dict(sorted(tempDict.items()))

file_name = (input("Input file name \n"
                   "Введите имя файла для сохранения: ") or "test")

folderToSaveJson = 'output/json_data/'
if not os.path.isdir(folderToSaveJson):
    os.mkdir(folderToSaveJson)

json.dump(plotsDict, open(folderToSaveJson + file_name + ".json", 'w'), indent=4)
#data = json.load( open( "file_name.json" ) )
#with open('data.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
#    data = json.load(fh) #загружаем из файла данные в словарь data

#вывод картинки графика for check
fig = plt.figure()
for lineParam, lineCoordinates in plotsDict.items():
    draw_plot(lineCoordinates, lineParam)
plt.savefig("_all.png")
plt.legend()
plt.show()

print('Get coordinates!')