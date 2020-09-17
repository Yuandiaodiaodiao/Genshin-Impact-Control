from screenshot.getscreen import getpicture
import matplotlib.pyplot as plt
import cv2
import aircv

temple = cv2.imread("D:\Github\Genshin-Impact-Control/img/targetbig.png", -1)

temple = cv2.cvtColor(temple, cv2.COLOR_BGRA2RGBA)
x, y = temple.shape[0:2]
bigval =1
temple = cv2.resize(temple, (int(y * bigval), int(x * bigval)))

def findTarget(img):
    h,w,_=img.shape


    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    res = aircv.find_template(img, temple, threshold=0.55)
    if res is None:return res
    res["result"]=tuple(map(int,res["result"]))

    cv2.circle(img, res["result"], 30,
               (255, 0, 0, 255), 5)
    plt.imshow(img)
    plt.show()
    return res
    # cv2.waitKey()
if __name__=="__main__":
    img = getpicture("原神")
    res=findTarget(img)
    print(res)
