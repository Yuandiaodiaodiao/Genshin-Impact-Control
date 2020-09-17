from screenshot.getscreen import getpicture
import cv2
import matplotlib.pyplot as plt


def getminiMap(img):
    L = 65
    R = 275
    T = 15
    B = 230
    crop = img[int(T):int(B), int(L):int(R)]
    return crop


def getMapCenter(img):
    offsetx = 50
    offsety = 50
    crop = img[img.shape[1] // 2 - offsetx:img.shape[1] // 2 + offsetx,
           img.shape[0] // 2 - offsety:img.shape[0] // 2 + offsety]
    return crop


def doBinary(img):
    crop = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    dst = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 111, -10)
    blurred = cv2.GaussianBlur(dst, (3, 3), 0)
    erode = cv2.erode(blurred, None, iterations=3)
    return erode


def solveFaceDirection(img):
    posx = 0
    posy = 0
    num = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 255:
                posx += i
                posy += j
                num += 1
    if num == 0:
        return 0, 0
    posx //= num
    posy //= num
    cv2.circle(img, (posy, posx), 10, 0, 1)
    centerx = img.shape[0] // 2
    centery = img.shape[1] // 2
    relx = posx - centerx
    rely = posy - centery
    return relx, rely


import cmath
import math


def solvePolayAngle(y, x):
    cn = complex(x, y)
    len, deg = cmath.polar(cn)
    deg = math.degrees(deg)
    deg = (deg - 90 + 720) % 360
    # print("极坐标角度=" + str(deg))
    return deg


import aircv

temple = cv2.imread("D:\Github\Genshin-Impact-Control\img/target.png", -1)
temple = cv2.cvtColor(temple, cv2.COLOR_BGRA2RGBA)
x, y = temple.shape[0:2]
bigval = 0.5
temple = cv2.resize(temple, (int(y * bigval), int(x * bigval)))


def getTargetPos(img):
    # cv2.imshow("",img)
    # cv2.waitKey()
    # cv2.imshow("",temple)
    # cv2.waitKey()
    # plt.subplot(121)
    # plt.imshow(img)
    # plt.subplot(122)
    # plt.imshow(temple)
    # plt.show()
    # cv2.waitKey()
    res = aircv.find_template(img, temple, threshold=0.6)
    # print(res)
    return res


def getTargetRelPos(degree):
    deg = math.radians(degree)
    cn1 = cmath.rect(50, deg)

    return cn1.real, cn1.imag


def getAllDegree():
    img = getpicture("原神")
    # cv2.imshow("",img)
    # cv2.waitKey()
    minimap = getminiMap(img)

    minimap = cv2.cvtColor(minimap, cv2.COLOR_BGRA2RGBA)

    cv2.circle(minimap, (minimap.shape[1] // 2, minimap.shape[0] // 2), 10,
               (0, 0, 0, 255), 5)

    targetInfo = getTargetPos(minimap)

    if targetInfo is not None:
        targetDegree = solvePolayAngle(targetInfo["result"][1] - minimap.shape[1] // 2,
                                       targetInfo["result"][0] - minimap.shape[0] // 2)
        targetX, targetY = targetInfo["result"]
    minimapCenter = getMapCenter(minimap)

    minimapBinary = doBinary(minimapCenter)

    posx, posy = solveFaceDirection(minimapBinary)

    degree = solvePolayAngle(posx, posy)
    if targetInfo is None:
        cv2.imshow("", minimapBinary)
        cv2.waitKey(1)
        return{
            "face":degree
        }
    else:

        print("Tdegree=" + str(degree - targetDegree))
        xT, yT = getTargetRelPos(targetDegree)
        imgshow = cv2.cvtColor(minimapBinary, cv2.COLOR_GRAY2RGB)
        targetX = int(targetX / minimap.shape[0] * imgshow.shape[0])
        targetY = int(targetY / minimap.shape[1] * imgshow.shape[1])
        # print((imgshow.shape[1] // 2, imgshow.shape[0] // 2), (int(targetY), int(targetX)))
        cv2.line(imgshow, (imgshow.shape[1] // 2, imgshow.shape[0] // 2), ((targetX)
                                                                           , int(targetY)),
                 (255, 0, 0), 4)

        cv2.imshow("", imgshow)
        cv2.waitKey(1)
        return {
            "target":targetDegree,
            "face":degree
        }

if __name__ == '__main__':
    while True:
        getAllDegree()
