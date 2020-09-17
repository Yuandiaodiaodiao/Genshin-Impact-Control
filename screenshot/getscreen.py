import time
import win32gui, win32ui, win32con, win32api
import ctypes.wintypes
import numpy as np
import cv2
def get_current_size(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        size = (rect.right - rect.left, rect.bottom - rect.top)
        return size


def gethwnd(hwname):
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        # if t is not "":
        #     print(h, t)
        if t == hwname:
            return h
    print(f"{hwname} 未找到")
    return 0




def window_capture(hw, filename, mode='window',FULLRES=[1920,1080]):
    hwnd = hw  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    if mode == "window" and hw>0:
        sizeobj = get_current_size(hwnd)

    else:
        hwnd=0
        hw=0
        sizeobj = FULLRES
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()

    w = sizeobj[0]
    h = sizeobj[1]
    # print(w,h)
    catchw = w
    catchh = h
    startw=0
    starth=0
    if w==1924 and h==1130:
        startw=2
        starth=1130-1080
        catchw=1922
        catchh=1130
        w=1920
        h=1080

    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (startw, starth), win32con.SRCCOPY)
    # bmbit=saveBitMap.GetBitmapBits(False)
    signedIntsArray = saveBitMap.GetBitmapBits(True)

    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img=np.reshape(img,(h,w,4))
    # cv2.imshow(",",img)
    # cv2.waitKey()
    # saveBitMap.SaveBitmapFile(saveDC, filename)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    return img


def getpicture(gamename, mode='window',FULLRES=[1920,1080]):
    hw = gethwnd(gamename)
    return window_capture(hw, gamename, mode,FULLRES)


if __name__ == "__main__":
    while True:
        beg = time.time()
        hw = gethwnd("原神")
        img=window_capture(hw, "./temp/screen.bmp")
        L=65;R=275;T=15;B=230
        crop=img[int(T):int(B),int(L):int(R)]
        minimap=crop
        cv2.circle(crop,(crop.shape[1]//2,crop.shape[0]//2),10,(0,0,0),5)

        offsetx=50
        offsety=50
        crop=crop[crop.shape[1]//2-offsetx:crop.shape[1]//2+offsetx, crop.shape[0]//2-offsety:crop.shape[0]//2+offsety]
        crop=cv2.cvtColor(crop,cv2.COLOR_RGB2GRAY)
        dst=cv2.adaptiveThreshold(crop,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,111,-10)
        blurred = cv2.GaussianBlur(dst, (3, 3), 0)
        erode=cv2.erode(blurred, None, iterations=3)
        posx=0;posy=0;num=0
        for i in range(erode.shape[0]):
            for j in range(erode.shape[1]):
                if erode[i][j]==255:
                    posx+=i
                    posy+=j
                    num+=1
        posx//=num
        posy//=num
        cv2.circle(erode,(posy,posx),10,0,1)
        centerx=erode.shape[0]//2
        centery=erode.shape[1]//2
        relx=posx-centerx
        rely=posy-centery
        import cmath
        import math
        cn = complex(relx, rely)
        print(cn)
        len,deg=cmath.polar(cn)
        deg=math.degrees(deg)
        deg=(deg-90+720)%360
        print("极坐标角度="+str(deg))
        cv2.imshow("",minimap)
        cv2.waitKey()
        end = time.time()
        print(end - beg)
