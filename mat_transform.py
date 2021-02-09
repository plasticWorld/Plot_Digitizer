import numpy as np
import os, shutil, cv2
import matplotlib.pyplot as plt


# def loadList():
#     # the filename should mention the extension 'npy'
#     tempNumpyArray=np.load("res/names.npy")
#     return tempNumpyArray.tolist()



# определение пути
directory = 'res/skeleton'
# получение списка файлов
files = os.listdir(directory)
# определение шаблона
mats = filter(lambda x: x.endswith('.png'), files)
filesAmount = 0
curveNames = [] # list in string format
for el in mats:
    filesAmount += 1
    curveNames.append(str(el)[:-4])

# можно коментить выполняется очень долго
##############################
# clear folder for matrix
# folder = 'res/matrix'
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))
#
#
# count = 0
# while count < filesAmount:
#     img = cv2.imread("res/skeleton/" + curveNames[count] + ".png")
#
#     with open("res/matrix/" + curveNames[count] + ".txt", 'w') as filehandle:
#         for listitem in img:
#             for elem in listitem:
#                 temp = str(elem)[1:-1]
#                 if temp == '0 0 0':
#                     filehandle.write('0')
#                 else:
#                     filehandle.write('1')
#                 filehandle.write('\t')
#             filehandle.write('\n')
#
#     count = count + 1
####################################

width_dim_begin, height_dim_begin = (input("Input initial of axes (1)wigth, (2)height (default: 0 0)\n"
                                           "Введите начальные значения осей графика через пробел: ") or "0 0").split()

width_dim, height_dim = (input("Input final values of axes (1)wigth, (2)height (default: 1 1)\n"
                               "Введите конечные значения осей графика через пробел: ") or "1 1").split()



space = int(input("Input space value (default: 10%)\n"
                  "Введите процент разреживания(каждый КАКОЙ столбец учитывается): ") or "10")

# round float to 2 digits after dot
widthDelta = round((float(width_dim) - float(width_dim_begin)), 2)
heightDelta = round((float(height_dim) - float(height_dim_begin)), 2)

# определение пути
directory = 'res/matrix'
# получение списка файлов
files = os.listdir(directory)
# определение шаблона
mats = filter(lambda x: x.endswith('.txt'), files)

plotsDict = {} # словарь словарей координат - внешний ключ - параметр кривой, внутренний - координата Х

for currentFile in mats:
    tempDict = {} # dict of x and y
    fname = directory + "/" + currentFile
    # print(currentFile[:-4]) -------- для значения внешнего ключа
    mat = []
    with open(fname) as f:
        for line in f:
            mat.append([int(x) for x in line.split()])

    tempMatrix = np.array(mat) # DO YOU REALLY NEED IT ???
    # tX - строки(600), tY - столбцы (800)
    tempY, tempX = np.nonzero(tempMatrix) # получаем список индексов не нулевых элементов
    #
    ratioScaleX = round((widthDelta / tempMatrix.shape[1]), 10)
    ratioScaleY = round((heightDelta / len(tempMatrix)), 10)

    space = int(len(tempMatrix[0]) / (tempMatrix.shape[1]*(space/100)))

    tempX = tempX * ratioScaleX
    tempY = heightDelta - tempY * ratioScaleY
    tempDict = dict(zip(tempX[0::space], tempY[0::space]))
    plotsDict[currentFile[:-4]] = dict(sorted(tempDict.items()))


fig = plt.figure(1)
for lineParam, lineCoordinates in plotsDict.items():
    # set plot view
    plt.plot(lineCoordinates.keys(), lineCoordinates.values(), label=lineParam, linewidth=1)
    plt.axis([float(width_dim_begin), float(width_dim), float(height_dim_begin), float(height_dim)])
    plt.grid(True)
plt.legend()
plt.savefig("1.png")
#plt.show()




print('All done!')



# for row in data:
#     print(' '.join([str(elem) for elem in row]))


# for row in data:
#     print(' '.join(list(map(str, row))))

