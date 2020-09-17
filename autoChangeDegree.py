import math
from screenshot.miniMap import getAllDegree
from serialServer import mouseTurnAround
from serialServer import keyDown
from serialServer import keyUp
import time
import random
import numpy as np
if __name__ == "__main__":
    time.sleep(2)
    ls=[]
    keyDown("w")
    for i in range(100):
        deg = getAllDegree()
        mouseTurnAround(3, 1, 360,-1)

        if deg is not None and deg.get("target"):
            degTarget = deg["target"]
            ls.append(degTarget)
    keyUp("w")
    average=np.mean(ls)
    faceCache=[]
    while True:
        deg = getAllDegree()
        if deg is not None:
            faceCache.append(deg["face"])
            if len(faceCache)>1:
                faceCache.pop(0)
            degFace=np.mean([np.mean(faceCache),faceCache[-1]])
            degTarget = average

            if (math.fabs(degTarget - degFace) < 1
                or math.fabs(degTarget + 360 - degFace) < 1
                or math.fabs(degTarget - (degFace + 360)) < 1):
               faceCache=[]
            else:
                direcT=degTarget-degFace
                # print(direcT)
                direcT=math.fabs(direcT)/direcT
                # print(direcT)
                time.sleep(0.5)
                mouseTurnAround(math.fabs(degTarget-degFace)/2,direcT,0,0)
