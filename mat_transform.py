import cv2
import numpy as np
import os
import csv



# def loadList():
#     # the filename should mention the extension 'npy'
#     tempNumpyArray=np.load("res/names.npy")
#     return tempNumpyArray.tolist()



# # определение пути
# directory = 'res/skeleton'
# # получение списка файлов
# files = os.listdir(directory)
# # определение шаблона
# mats = filter(lambda x: x.endswith('.png'), files)
# filesAmount = 0
# for el in mats:
#     filesAmount += 1

# count = 0
# while count <= filesAmount:
#     img = cv2.imread("res/skeleton/test" + str(count) + ".png")
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # with open("res/matrix/test" + str(count) + ".txt", 'w') as filehandle:
    #     for listitem in img:
    #         for elem in listitem:
    #             temp = str(elem)[1:-1]
    #             if temp == '0 0 0':
    #                 filehandle.write('0')
    #             else:
    #                 filehandle.write('1')
    #             filehandle.write('\t')
    #         filehandle.write('\n')
    #
    # count = count + 1

width_dim_begin, height_dim_begin = (input("Input initial of axes (1)wigth, (2)height (default: 0 0)\n"
                                           "Введите начальные значения осей графика через пробел: ") or "0 0").split()

width_dim, height_dim = (input("Input final values of axes (1)wigth, (2)height (default: 1 1)\n"
                               "Введите конечные значения осей графика через пробел: ") or "1 1").split()

space = int(input("Input space value (default: 5)\n"
                  "Введите процент разреживания: ") or "5")

# round float to 2 digits after dot
widthDelta = round((float(width_dim) - float(width_dim_begin)), 2)
heightDelta = round((float(height_dim) - float(height_dim_begin)), 2)

# определение пути
directory = 'res/matrix'
# получение списка файлов
files = os.listdir(directory)
# определение шаблона
mats = filter(lambda x: x.endswith('.txt'), files)

plotsDict = dict() # словарь словарей координат - внешний ключ - параметр кривой, внутренний - координата Х

for currentFile in mats:
    tempDict = dict()
    fname = directory + "/" + currentFile
    # print(currentFile[:-4]) -------- для значения внешнего ключа
    mat = []
    with open(fname) as f:
        for line in f:
            mat.append([int(x) for x in line.split()])

    tempMatrix = np.array(mat) # DO YOU REALLY NEED IT ????????
    ratioScaleX = round((widthDelta / len(tempMatrix)), 10)
    ratioScaleY = round((heightDelta / len(tempMatrix[0])), 10)

    for i in range(len(tempMatrix)-1): # начинаем перебор с строк
        tempY = round(float((i * ratioScaleY)), 10) #

        for j in range(0, len(tempMatrix[i])-1, space): # прореживание происходит здесь
            print(j)
            tempX = round(float((j * ratioScaleX)), 10)
            if tempMatrix[i][j] > 0:
                tempDict[tempX] = tempY # save to inner dict





    #print(len(a))
    #print(len(a[0]))



print('All done!')
#cv2.waitKey(0)


# for row in data:
#     print(' '.join([str(elem) for elem in row]))


# for row in data:
#     print(' '.join(list(map(str, row))))

