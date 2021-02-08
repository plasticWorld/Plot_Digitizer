import cv2
import numpy as np
from skimage.morphology import skeletonize
import os



# def saveList(myList):
#     # the filename should mention the extension 'npy'
#     np.save("res/names.npy", myList)


def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


# mouse callback function for line drawing
def line_drawing(event,x,y,flags,param):
    img = imgMask
    global pt1_x,pt1_y,drawing

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            cv2.line(img,(pt1_x,pt1_y),(x,y),color=brushColor,thickness=brushSize)
            pt1_x,pt1_y=x,y
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        cv2.line(img,(pt1_x,pt1_y),(x,y),color=brushColor,thickness=brushSize)

def img_scaling(scale):
    img = imgColour.copy()
    height, width = img.shape[:2]  # image dimentions

    # масштабируем до 600рх по длинной стороне
    if height >= width:
        width = int(width * scale / height)
        height = scale
    else:
        height = int(height * scale / width)
        width = scale
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    return img

# mouse callback fun for put marks
def dots_drawing(event, x, y, flags, param):
    img = imgTemp

    global pt1_x, pt1_y, drawing
    # pt1_x, pt1_y - кликнутые координаты
    # x, y - координаты курсора мышки

    # поставить точку - нажать левую книпку мыши
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1_x, pt1_y = x, y
        cv2.circle(img, (pt1_x, pt1_y), radius=8, color=(255, 0, 0), thickness=1)
        cv2.line(img, (pt1_x, pt1_y), (pt1_x + 10, pt1_y + 10), (255, 0, 0), 1)
        cv2.line(img, (pt1_x, pt1_y), (pt1_x - 10, pt1_y - 10), (255, 0, 0), 1)
        cv2.line(img, (pt1_x, pt1_y), (pt1_x - 10, pt1_y + 10), (255, 0, 0), 1)
        cv2.line(img, (pt1_x, pt1_y), (pt1_x + 10, pt1_y - 10), (255, 0, 0), 1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    # подтвердить и внести в координаты - нажать правую кнопку мыши
    elif event == cv2.EVENT_RBUTTONDOWN:
        dim_x.append(pt1_x)
        dim_y.append(pt1_y)


def cropping_img(height, width):

    cv2.namedWindow("Cropping2")  # window for managing of resizing with trackers
    cv2.resizeWindow("Cropping2", width, 250)

    cv2.createTrackbar("W Begin", "Cropping2", 5, width, empty)
    cv2.createTrackbar("W End", "Cropping2", width - 5, width, empty)
    cv2.createTrackbar("H Begin", "Cropping2", 5, height, empty)
    cv2.createTrackbar("H End", "Cropping2", height - 5, height, empty)

    while True:
        img = imgResizing.copy()
        min_width = cv2.getTrackbarPos("W Begin", "Cropping2")
        max_width = cv2.getTrackbarPos("W End", "Cropping2")
        min_height = cv2.getTrackbarPos("H Begin", "Cropping2")
        max_height = cv2.getTrackbarPos("H End", "Cropping2")
        lineThickness = 1  # cv2.getTrackbarPos("Thickness", "Cropping") + 1

        cv2.line(img, (min_width, min_height), (min_width, max_height), (255, 255, 0), 1)  # left vertical line
        cv2.line(img, (min_width, min_height), (max_width, min_height), (255, 255, 0), 1)  # up horizontal line
        cv2.line(img, (max_width, min_height), (max_width, max_height), (255, 255, 0), 1)  # right vertical line
        cv2.line(img, (min_width, max_height), (max_width, max_height), (255, 255, 0), 1)  # down horizontal line

        #  # crop image
        cv2.imshow("Cropping2", img)  # show image in the same window as tracker

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return img[min_height:max_height, min_width:max_width]


imgGet = cv2.imread('res/img2.jpg', cv2.IMREAD_COLOR)#get image from file
imgColour = imgGet.copy()#cv2.cvtColor(imgGet, cv2.COLOR_GRAY2BGR) # assign color model


scale = int(input("Input window size in px (default=800)\n"
                  "Введите размер окна в пикселях: ") or "800") # scale in px
imgColour = img_scaling(scale) # to fit at monitor

# get borders for tracker
height, width = imgColour.shape[:2]

img_ratio = float(input("Input aspects ratio of image (default: 3/4)\n"
                        "Введите соотношение высота/ширина: ") or "0.75")

if width > height:
    height = int(scale * img_ratio)
else:
    width = int(scale * img_ratio)

drawing = False # true if mouse is pressed
pt1_x, pt1_y = None , None
dim_x, dim_y = [], []

wrap = bool(input("Do you need a wrap perspective? (default: False)\n"
                  "Необходимо исправить перпективу (1)да (Enter)нет: ") or False)

if wrap:
    imgTemp2 = imgColour.copy()
    img_dots_temp = imgColour.copy()
    img_dots_temp[:]=255, 255, 255

    cv2.namedWindow("Cropping")
    cv2.setMouseCallback("Cropping", dots_drawing)
    while len(dim_x) < 4:
        imgTemp = imgColour
        cv2.imshow("Cropping", imgTemp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    cv2.line(img_dots_temp, (dim_x[0], dim_y[0]), (dim_x[2], dim_y[2]), (255, 0, 255), 2)  # left vertical line
    cv2.line(img_dots_temp, (dim_x[0], dim_y[0]), (dim_x[1], dim_y[1]), (255, 0, 255), 2)  # up horizontal line
    cv2.line(img_dots_temp, (dim_x[1], dim_y[1]), (dim_x[3], dim_y[3]), (255, 0, 255), 2)  # right vertical line
    cv2.line(img_dots_temp, (dim_x[2], dim_y[2]), (dim_x[3], dim_y[3]), (255, 0, 255), 2)  # down horizontal line
    img_dots_temp = cv2.bitwise_and(imgTemp2, img_dots_temp)

    pts1 = np.float32([[dim_x[0], dim_y[0]],[dim_x[1], dim_y[1]],[dim_x[2], dim_y[2]],[dim_x[3], dim_y[3]]])
    pts2 = np.float32([[0, 0],[width, 0],[0, height],[width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgResizing = cv2.warpPerspective(imgTemp2, matrix, (width, height))
else:
    imgResizing = imgColour.copy()
    img_dots_temp = imgColour.copy()

img2 = cropping_img(height, width)
height, width = img2.shape[:2]

imgSt = stackImages(0.5, ([img_dots_temp, img2],[imgResizing, img2]))
cv2.imshow("out3", imgSt)
cv2.waitKey(0)
cv2.destroyAllWindows()

dots = bool(input("Do you want to use a brush or set dots? (default: brush)\n"
                  "Отслеживать линию кистью или проставить точки? (1)точки (Enter)кисть: ") or False)


if dots:
    i = 0
else:
    while True:
        imgMask = img2.copy()
        imgMask[:]=255,255,255 # make image white

        brushSize = int(input("Input a size of brush (default: 20)\n"
                              "Введите размер кисти: ") or "20") # size of brush while drawing lines

        cv2.namedWindow("Colouring")
        brushColor = (0, 0, 255)
        cv2.setMouseCallback("Colouring", line_drawing)

        while True:
            imgOverlay = cv2.bitwise_and(img2, imgMask)
            cv2.imshow("Colouring", imgOverlay)
            if cv2.waitKey(1) & 0xFF == ord ('q'):
                break
        cv2.destroyAllWindows()

        imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY) #translate from bgr to gray color scheme
        (thresh, imgBWMask) = cv2.threshold(imgMask, 127, 255, cv2.THRESH_BINARY_INV) # making it black/white
        imgOriginal_inv = cv2.bitwise_not(img2)
        imgMaskFinal = cv2.cvtColor(imgBWMask, cv2.COLOR_GRAY2BGR)

        imgLine = cv2.bitwise_and(imgOriginal_inv, imgMaskFinal) # use mask and get extract line img
        imgLine = cv2.bitwise_not(imgLine)
        imgLine = cv2.cvtColor(imgLine, cv2.COLOR_BGR2GRAY)

        thresholdValue = 10
        cv2.namedWindow("Thresholing")
        cv2.resizeWindow("Thresholing", width, height)
        cv2.createTrackbar("Threshold", "Thresholing", thresholdValue, 250, empty)

        while True:
            imgCrop = imgLine.copy()  # load new copy every cycle
            thresholdValue = cv2.getTrackbarPos("Threshold", "Thresholing") # getting value from tracker
            ret, imgCrop = cv2.threshold(imgCrop, thresholdValue, 255, 0) # thresholding image
            cv2.imshow("Thresholing", imgCrop) # show image in the same window as tracker
            if cv2.waitKey(1) & 0xFF == ord ('q'):
                break

        imgCrop = cv2.bitwise_not(imgCrop)

        skeleton_lee = skeletonize(imgCrop, method='lee')

        (thresh, imgToSave) = cv2.threshold(skeleton_lee, 127, 255, cv2.THRESH_BINARY) # making it black/white

        cv2.destroyAllWindows()

        cv2.namedWindow("Colouring")
        brushColor = (0, 0, 0)
        brushSize = 10
        imgMask = imgToSave
        cv2.setMouseCallback("Colouring", line_drawing)

        while True:
            imgToSave = imgMask
            cv2.imshow("Colouring", imgToSave)
            if cv2.waitKey(1) & 0xFF == ord ('q'):
                break
        cv2.destroyAllWindows()

        curveName = input("Input curve name (default: 0)\n"
                          "Введите параметр линии(числовой) при значении которого выберут данную кривую: ") or "0"

        # clear folder for img
        filelist = [f for f in os.listdir("res/skeleton") if f.endswith(".png")]
        for f in filelist:
            os.remove(os.path.join("res/skeleton", f))

        cv2.imwrite("res/skeleton/" + curveName + ".png", imgToSave)  # png or tif support 16bit !
        imgToSave = cv2.cvtColor(imgToSave, cv2.COLOR_GRAY2BGR)

        nextLine = bool(input("Do you want to extract next line? (default: no)\n"
                              "Отслеживать линию кистью или проставить точки? (1)следующая (Enter)закончить: ") or False)
        if not nextLine:
            break


print('All done!')


#linesAmount = int(input("How many lines You want to extract? ") or "1") # cycle up limit
#imgMask = np.zeros((height,width,3),np.uint8) # create blank image with zeros - black

# cv2.imshow("Img to save", imgToSave)
# cv2.waitKey(0)
# imgToSave = cv2.cvtColor(skeleton_lee, cv2.COLOR_BGR2GRAY) #translate from bgr to gray color scheme

# imgCrop = imgCrop[heightBegin:heightEnd, widthBegin:widthEnd] # crop image