from screenshot.status import ifConversation
from screenshot.getscreen import getpicture
from serialServer import press
if __name__=="__main__":
    while True:
        img = getpicture("原神")
        res = ifConversation(img)
        if res:
            press(" ")