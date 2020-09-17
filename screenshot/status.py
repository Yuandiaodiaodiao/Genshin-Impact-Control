from screenshot.getscreen import getpicture
import cv2
import aircv

temple = cv2.imread("D:\Github\Genshin-Impact-Control\img\conversation.png", -1)
temple = cv2.cvtColor(temple, cv2.COLOR_BGRA2RGBA)
x, y = temple.shape[0:2]
bigval = 0.5
temple = cv2.resize(temple, (int(y * bigval), int(x * bigval)))

def ifConversation(img):
    h,w,_=img.shape

    dialogbox=img[int(h*0.95):,w//2-25:w//2+25]
    dialogbox = cv2.cvtColor(dialogbox, cv2.COLOR_BGRA2RGBA)
    cv2.imshow("",dialogbox)
    cv2.waitKey()
    res = aircv.find_template(dialogbox, temple, threshold=0.45)
    print(res)
    if res :
        return True
    return False
    # cv2.imshow("",dialogbox)
    # cv2.waitKey()
if __name__=="__main__":
    img = getpicture("原神")
    res=ifConversation(img)
    print(res)