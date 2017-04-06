import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

BOARDSTART = 50
BOARDSPACE = 40
BOARDEND = BOARDSTART + 18*BOARDSPACE
STONERADIUS = BOARDSPACE/2
WHITESTONE = "white"
BLACKSTONE = "black"

curser_x = None
curser_y = None

class Stone(object):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def if_white(self):
        if t == WHITESTONE:
            return True
        else:
            return False

    def xx(self):
        print("x = " + str(self.x))
        return self.x

    def yy(self):
        return self.y

class StoneList(object):
    def __init__(self):
        self.stone_list = [[]]
        # self.curser_x = 0
        # self.curser_y = 0
        # self.end = True

    def addStone(self, s):
        list = [s]
        if(len(self.stone_list[0]) == 0):
        	self.stone_list[0].append(s)
        else:
        	self.stone_list.append(list)
        print("stone added")
        print("new stone x:" + str(list[0].xx()))

    def showNext(self, x, y):
        global curser_x
        global curser_y

        print(str(x))
        if(y < len(self.stone_list[x]) - 1):
            curser_y = y + 1
        elif(x < len(self.stone_list) - 1):
            curser_x = x + 1
            curser_y = 0
        else:
            curser_x = None
            curser_y = None
        print("curser_x" + str(curser_x) + "curser_y" + str(curser_y))
        print(self.stone_list[x][y].xx())
        return(self.stone_list[x][y])

game_go = StoneList()

class StockDialog(QWidget):
    def __init__(self, parent = None):
        super(StockDialog, self).__init__(parent)
        self.setWindowTitle("go")
        
        mainSplitter1 = QSplitter(Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)
        
        stack1 = QStackedWidget()
        stack1.setFrameStyle(QFrame.Panel|QFrame.Raised)
        self.area = GameBoard()
        stack1.addWidget(self.area)        
        frame1 = QFrame(mainSplitter1)
        mainLayout1 = QVBoxLayout(frame1)
        #mainLayout1.setMargin(10)
        mainLayout1.setSpacing(6)
        mainLayout1.addWidget(stack1)

        layout = QGridLayout(self)
        layout.addWidget(mainSplitter1,0,0)
        # layout.addWidget(mainSplitter,0,1)
        self.setLayout(layout)
        
    
class GameBoard(QWidget):
    def __init__(self):
        super(GameBoard,self).__init__()
        self.setWindowTitle("go")
        self.Shape = ["Line","Rectangle", 'Rounded Rectangle', "Ellipse", "Pie", 'Chord', 
    "Path","Polygon", "Polyline", "Arc", "Points", "Text", "Pixmap"]
        self.setPalette(QPalette(QColor("#dfb473")))
        self.setAutoFillBackground(True)
        self.setMinimumSize(800,800)
        self.pen = QPen()
        self.brush = QBrush()        

        self.press_x = 30
        self.press_y = 30
        self.press_flag = 0
    
    def paintEvent(self, QPaintEvent):
        global curser_x
        global curser_y
        p = QPainter(self)
        p.setPen(QPen(Qt.black))

        for i in range(0, 19):
            p.drawLine(QPoint(BOARDSTART, BOARDSTART + BOARDSPACE*i), QPoint(BOARDEND, BOARDSTART + BOARDSPACE*i))
            p.drawLine(QPoint(BOARDSTART + BOARDSPACE*i, BOARDSTART), QPoint(BOARDSTART + BOARDSPACE*i, BOARDEND))

        linearGradient = QLinearGradient(0,0,400,400)
        linearGradient.setColorAt(0.0, Qt.black)
        p.setBrush(linearGradient)
        rect = QRect(BOARDSTART + 3*BOARDSPACE - 3, BOARDSTART + 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDEND - 3*BOARDSPACE - 3, BOARDSTART + 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDSTART + 3*BOARDSPACE - 3, BOARDEND - 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDEND - 3*BOARDSPACE - 3, BOARDEND - 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDEND - 9*BOARDSPACE - 3, BOARDEND - 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDSTART + 9*BOARDSPACE - 3, BOARDSTART + 3*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDEND - 3*BOARDSPACE - 3, BOARDEND - 9*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDSTART + 3*BOARDSPACE - 3, BOARDEND - 9*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)
        rect = QRect(BOARDSTART + 9*BOARDSPACE - 3, BOARDEND - 9*BOARDSPACE - 3, 6, 6)
        p.drawRect(rect)

        # draw black stones
        print("update after pressing")

        p.setPen(QPen(Qt.black))
        linearGradient = QLinearGradient(0, 0, 400, 400)
        linearGradient.setColorAt(0.0, Qt.black)
        p.setBrush(linearGradient)
        while curser_x != None or curser_y != None:
            self.press_flag = 0
            temp = game_go.showNext(curser_x, curser_y)
            x = temp.xx() - 1
            y = temp.yy() - 1
            print("sssscurser_x" + str(curser_x) + "curser_y" + str(curser_y))
            rect = QRect(x*BOARDSPACE - BOARDSPACE/2 + BOARDSTART, y*BOARDSPACE - BOARDSPACE/2 + BOARDSTART, 40, 40)
            p.drawPie(rect, 0 * 16, 360 * 16)

    def mousePressEvent(self, event):
        global curser_x
        global curser_y
        curser_x = 0
        curser_y = 0
        x = event.x()
        y = event.y()
        # self.press_x = (int((x - BOARDSTART + BOARDSPACE/2)/BOARDSPACE))*BOARDSPACE - BOARDSPACE/2 + BOARDSTART
        # self.press_y = (int((y - BOARDSTART + BOARDSPACE/2)/BOARDSPACE))*BOARDSPACE - BOARDSPACE/2 + BOARDSTART
        s = Stone(int((x + BOARDSPACE/2)/BOARDSPACE), int((y + BOARDSPACE/2)/BOARDSPACE), BLACKSTONE)
        print("new stone!!!: " + str(s.xx()))
        game_go.addStone(s)
        curser_x = 0
        curser_y = 0
        self.update()

if __name__=='__main__':
    app = QApplication(sys.argv)
    form = GameBoard()
    form.move(200, 100)
    form.show()
    app.exec_()