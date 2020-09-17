# Genshin-Impact-Control
arduino控制鼠标键盘完成对原神的脚本输入 opencv自动寻路  
 
原神也就图一乐 真要国产之光还得看 strike buster prototype  

通过arduino due的MCU通信 可以作为usb设备插入到主机上配合官方自带的Mouse Keyboard库来模拟键鼠  
然后用串口进行通信  
寻路用cv2的自适应二值化可以在小地图上找到人物的朝向  
通过对那个黄色图标的搜图可以找到目标方向 由于可以爬墙所以走就完事了  
不过要是想更优的话就只能写死路径比如走多少秒转多少度这种  
鼠标模拟的稳定性可以让人物转20圈误差1度左右  
演示:https://tieba.baidu.com/p/6950876347?share=9105&fr=share&see_lz=0&sfc=copy&client_type=2&client_version=11.0.0.0&st=1600343877&unique=827FE2A948083D4F2F124A23F662C367&red_tag=3531308824  
