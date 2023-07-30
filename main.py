from PyQt5 import QtWidgets as q,uic,QtCore
from PyQt5.QtGui import QIcon
from sys import argv,exit as e
from os import path
from colorsys import hsv_to_rgb,rgb_to_hsv
class Functions:
    def hsvToRgb(self,h:float, s:float, v:float)->tuple:
        r, g, b = hsv_to_rgb(h/100 , s/100 , v/100)
        return r * 255, g * 255, b * 255
    def hexToRgb(self,hexColor:str)->tuple:
        if len(hexColor)<6:hexColor+="0"*(6-len(hexColor))
        r,g,b=(int(hexColor[i:i+2],16) for i in (0,2,4))
        return r,g,b
    def rgbToCmyk(self,r:int,g:int,b:int)-> int:
        c,m,y=1-(r/255),1-(g/255),1-(b/255)
        k=min(c,m,y)
        if k==1:return (0,0,0,1)
        c=(c-k)/(1-k)
        m=(m-k)/(1-k)
        y=(y-k)/(1-k)
        return round(c*100),round(m*100),round(y*100),round(k*100)
    def rgbToHsv(self,r:int,g:int,b:int):
        h,s,v=rgb_to_hsv(r/255,g/255,b/255)
        return h*100,s*100,v*100
    def hexChanged(self):
        hexColor=self.hexColorEntry.text()
        if hexColor.startswith("#"):
            hexColor=hexColor[1:]
            try:int(hexColor,16)
            except:pass
            else:
                r,g,b=self.hexToRgb(hexColor)
                h,s,v=self.rgbToHsv(r,g,b)  
                v,x,y=int(h*3.60),int(s*5.60),200-int(v*2.0)
                self.colorSlider.valueChanged.disconnect(self.changeColor)
                self.colorSlider.setValue(v)
                self.colorSlider.valueChanged.connect(self.changeColor)
                self.colorSelector.move(QtCore.QPoint(x,y))
                self.changeColor(1)
    def changeColor(self,ignore=None):
        h,s,v=(self.colorSlider.value()/3.60,self.colorSelector.x()/5.60,(200-self.colorSelector.y())/2.0)
        r,g,b=self.hsvToRgb(h,s,v)
        r,g,b=round(r),round(g),round(b)
        c,m,y,k=self.rgbToCmyk(r,g,b)
        self.viewColorFrame.setStyleSheet(f"background:rgb({r},{g},{b});border-radius:0px")
        self.colorFrame.setStyleSheet(f"background-color: qlineargradient(x1:1, x2:0, stop:0 hsv({h}%,100%,100%), stop:1 #fff);border-radius:0px")
        self.colorSlider.setStyleSheet(f"""
        QSlider::groove:horizontal {{
    border-radius:4px;
    height: 10px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));	
}}
QSlider::handle:horizontal {{
    background-color: hsv({h}%,100%,100%);
    border: 2px solid black;
    height: 20px;
    width: 26px;
    margin: -10 0;
    border-radius: 14px;
}}""")  
        if ignore!=1:self.hexColorEntry.setText(f"#{r:02x}{g:02x}{b:02x}")
        self.rgbColorEntry.setText(f"{r},{g},{b}")
        self.cmykEntry.setText(f"{c}%,{m}%,{y}%,{k}%")
        self.hsvEntry.setText(f"{self.colorSlider.value()}°,{round(s)}%,{round(v)}%")
class colorPicker(q.QMainWindow,Functions):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui",self)
        self.setWindowTitle("Color Picker")
        if path.exists("windowIcon.png"):self.setWindowIcon(QIcon("windowIcon.png"))
        self.setMinimumSize(784,507)
        self.headerFrame.mouseMoveEvent=self.moveWindow
        self.colorSelect.mouseMoveEvent=self.selectColor
        self.colorSelect.mousePressEvent=self.selectColor
        self.colorSlider.valueChanged.connect(self.changeColor)
        self.hexColorEntry.textEdited.connect(self.hexChanged)
        self.hexColorEntry.setMaxLength(7)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
        self.exitButton.clicked.connect(self.close)
        self.minimizeButton.clicked.connect(self.showMinimized)
    def selectColor(self,event):
        pos=event.pos()
        if pos.x()<0:pos.setX(0)
        if pos.y()<0:pos.setY(0)
        if pos.x()>560:pos.setX(560)
        if pos.y()>200:pos.setY(200)
        self.colorSelector.move(pos)
        self.changeColor()
    def mousePressEvent(self,event):
        self.clickPosition=event.globalPos()
    def moveWindow(self,event):
        if not self.isMaximized() and event.buttons()==QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos()+event.globalPos()-self.clickPosition)
            self.clickPosition=event.globalPos()
            event.accept()      
if __name__=="__main__":
    app = q.QApplication(argv)
    w = colorPicker()
    w.show()
    e(app.exec_())
