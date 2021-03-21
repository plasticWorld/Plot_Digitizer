import numpy as np
import os, json
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from main import check_folder_exist


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
res_filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
with open(res_filename, 'r', encoding='utf-8') as fh: #открываем файл на чтение
    data = json.load(fh) #загружаем из файла данные в словарь data


new_data = {} # create new dictionary with different structure
for lineParam, lineCoordinates in data.items():
    a = []
    for x, y in lineCoordinates.items():
        b = (float(x), y) # both line coordinates have type float now
        a.append(b)
    new_data[lineParam] = a

folderToSaveJson = 'res/output_json_pairs/'
check_folder_exist(folderToSaveJson)
# if not os.path.isdir(folderToSaveJson):
#     os.mkdir(folderToSaveJson)
parts = res_filename.rsplit('/', 2)  # отрезаем от пути только имя
json.dump(new_data, open(folderToSaveJson + parts[2], 'w'), indent=4)

fig = plt.figure()
for lineParam, lineCoordinates in new_data.items():

    plt.xticks(np.arange(0, 60, step=5))
    #plt.yticks(np.arange(0, 50, step=5))
    x, y = [], []
    for a, b in lineCoordinates:
        x.append(a)
        y.append(b)
    plt.plot(x, y, label=lineParam, linewidth=1)

folderToSaveImg = 'res/output_img/'
check_folder_exist(folderToSaveImg)
# if not os.path.isdir(folderToSaveImg):
#     os.mkdir(folderToSaveImg)
res = parts[2].rsplit('.', 1)
plt.savefig(str(folderToSaveImg)+str(res[0])+".png")