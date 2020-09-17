import serial

def getAvailableCom(defult=""):
    import serial.tools.list_ports
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
    else:
        port_list.reverse()
        if any(map(lambda x:defult in x,port_list)):
            return defult
        for i in port_list:
            if "串行设备" in i:
                return i.split(" ")[0]

com=getAvailableCom("COM7")

def createSerial(portx,bps=19200):
    try:
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）

        # 打开串口，并得到串口对象
        print(portx)
        portx="COM7"
        ser = serial.Serial(portx, bps,dsrdtr=True)
        print(ser.is_open)
        return ser
        # 写数据
        # print("写总字节数:", result)
        #
        # ser.close()  # 关闭串口

    except Exception as e:
        print("---异常---：", e)

serials=createSerial(com)
print(serials)

def mouseMoveH():
    serials.write("1 100 100 ".encode('gbk'))

def mouseMove(x,y):
    serials.write(f"1 {x} {y} ".encode('gbk'))

def press(key):
    serials.write(f"2 {key} ".encode("gbk"))
def keyDown(key):
    serials.write(f"3 {key} ".encode("gbk"))
def keyUp(key):
    serials.write(f"4 {key} ".encode("gbk"))
import time
time.sleep(2)


# for i in range(2):
# mouseMoveH()
# import time
#
# time.sleep(2)
import math
roundPos=4117
def mouseTurnAround(degreex,posx,degreey=0,posy=0):
    roundAxis=126
    roundLast=roundPos*(degreex/360)
    while roundLast>0:
        # time.sleep(0.05)
        rx=roundAxis if roundAxis<=roundLast else roundLast
        roundLast-=rx
        mouseMove(round(posx*rx),round(posy*roundAxis*(degreey/360)))


# for i in range(20):
#     # time.sleep(0.01)
#     mouseTurnAround(360,-1)
    # mouseTurnAround(360,1)
# serials.close()
