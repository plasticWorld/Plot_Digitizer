import numpy as np
import os, cv2
import matplotlib.pyplot as plt


def loadList(folder):
    # получение списка файлов
    files = os.listdir(folderToFindImg)
    # определение шаблона
    names = filter(lambda x: x.endswith('.png'), files)
    return names

def transform_coordinates(space, tempMatrix, widthDelta, heightDelta):
    # tX - строки(600), tY - столбцы (800)
    tempY, tempX = np.nonzero(tempMatrix) # получаем список индексов не нулевых элементов

    # getting plot scale coef by axis
    ratioScaleX = round((widthDelta / tempMatrix.shape[1]), 10)
    ratioScaleY = round((heightDelta / len(tempMatrix)), 10)
    # percent of sparseness
    space = int(len(tempMatrix[0]) / (tempMatrix.shape[1]*(space/100)))
    # getting real plot coordinates of x and y

    tempX = (tempX * ratioScaleX).round(5)

    tempY = ((tempMatrix.shape[0] - tempY) * ratioScaleY ).round(5)#+ heightDelta

    # add to temp dict structure x as key and y as value
    tempDict = dict(zip(tempX[0::space], tempY[0::space]))
    return tempDict


width_dim_begin, height_dim_begin = (input("Input initial of axes (1)wigth, (2)height (default: 0 0)\n"
                                           "Введите минимальные значения осей графика через пробел: ") or "0 0").split()

width_dim, height_dim = (input("Input final values of axes (1)wigth, (2)height (default: 1 1)\n"
                               "Введите максимальные значения осей графика через пробел: ") or "1 1").split()

space = int(input("Input space value (default: 10%)\n"
                  "Введите процент разреживания(каждый КАКОЙ столбец учитывается): ") or "10")

# round float to 2 digits after dot
widthDelta = round((float(width_dim) - float(width_dim_begin)), 2)
heightDelta = round((float(height_dim) - float(height_dim_begin)), 2)

# определение пути
folderToFindImg = 'res/skeleton/'
filesNames = loadList(folderToFindImg)

# словарь словарей координат - внешний ключ - параметр кривой, внутренний - координата Х
plotsDict = {}

for currentFile in filesNames:
    tempMatrix = cv2.imread(folderToFindImg + currentFile, 0)  # 0 - for gray color scheme:(0, 255)
    tempDict = transform_coordinates(space, tempMatrix, widthDelta, heightDelta)
    # add dict of plot coordinates to final dict with curve name(digital) as key
    plotsDict[currentFile[:-4]] = dict(sorted(tempDict.items()))


fig = plt.figure()
for lineParam, lineCoordinates in plotsDict.items():
    # set plot view
    plt.plot(lineCoordinates.keys(), lineCoordinates.values(), label=lineParam, linewidth=1)
    x1, x2, y1, y2 = 0,0,0,0

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

    #plt.axis([x1, x2, y1, y2])
    plt.grid(True)
plt.legend()
plt.savefig("1.png")
print('Get coordinates!')