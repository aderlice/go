import sys
import pdb
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

BOARDSTART = 50
BOARDSPACE = 40
BOARDEND = BOARDSTART + 18*BOARDSPACE
STONERADIUS = BOARDSPACE/2
WHITESTONE = "white"
BLACKSTONE = "black"

# curser_x = None
# curser_y = None

class Stone(object):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

    def if_white(self):
        if self.t == WHITESTONE:
            return True
        else:
            return False

    def xx(self):
        return self.x

    def yy(self):
        return self.y

class StoneList(object):
    def __init__(self):
        self.stone_list = [[]]
        self.curser_x = 0
        self.curser_y = 0
        self.end = True
        self.turn = BLACKSTONE
        self.msg = False

    def isMsg(self):
        if self.msg == True:
            self.msg = False
            return(True)
        else:
            return(False)

    def isExist(self, x, y):
        for i in self.stone_list:
            for j in i:
                if j.xx() == x and j.yy() == y:
                    return True
        return False

    def isAlive(self, t):
        flag = 1
        for i in self.stone_list:
            for j in i:
                if j.if_white() == True and t == BLACKSTONE or j.if_white() == False and t == WHITESTONE:
                    flag = 0
                    break
                if  (j.xx() - 1 == 0 or self.isExist(j.xx() - 1, j.yy()) == True) and (j.xx() + 1 == 20 or self.isExist(j.xx() + 1, j.yy()) == True) and (j.yy() - 1 == 0 or self.isExist(j.xx(), j.yy() - 1) == True) and (j.yy() + 1 == 20 or self.isExist(j.xx(), j.yy() + 1) == True):
                    flag = flag * 1
                else:
                    flag = flag * 0
            if flag == 1:
                return(False)
            flag = 1
        return(True)

    def capStones(self, t):
        flag = 1
        # pdb.set_trace()
        for i in self.stone_list:
            for j in i:
                if j.if_white() == True and t == BLACKSTONE or j.if_white() == False and t == WHITESTONE:
                    flag = 0
                    break
                if  (j.xx() - 1 == 0 or self.isExist(j.xx() - 1, j.yy()) == True) and (j.xx() + 1 == 20 or self.isExist(j.xx() + 1, j.yy()) == True) and (j.yy() - 1 == 0 or self.isExist(j.xx(), j.yy() - 1) == True) and (j.yy() + 1 == 20 or self.isExist(j.xx(), j.yy() + 1) == True):
                    flag = flag * 1
                else:
                    flag = flag * 0
            if flag == 1:
                self.stone_list.remove(i)
            flag = 1

    def isEnd(self):
        return self.end

    def resetEnd(self):
    	self.end =False

    def isConnect(self, x, y, x0, y0):
        if ((x - x0)*(x - x0) + (y - y0)*(y - y0)) == 1:
            return True
        else:
            return False

    def get_curser_x(self):
        return self.curser_x

    def get_curser_y(self):
        return self.curser_y

    def get_turn(self):
        return self.turn

    def addStone(self, x, y):
        if self.isExist(x, y) == True:
            self.msg = True
            return
        s = Stone(x, y, self.turn)
        origin = [[]]
        for i in self.stone_list:
            origin.append(i)
        temp_list1 = [s]
        temp_list = [[]]
        self.end = False
        temp_turn = self.turn
        if self.turn == BLACKSTONE:
            self.turn = WHITESTONE
        else:
            self.turn = BLACKSTONE
        print("self.turn:" + str(self.turn))
        print("temp_turn:" + str(temp_turn))
        if(len(self.stone_list[0]) == 0):
            self.stone_list[0].append(s)
            return
        flag = False
        # pdb.set_trace()
        # rearange list

        print("origin:")
        for i in self.stone_list:
            for j in i:
                print("(" + str(j.xx()) + " ," + str(j.yy()) + ")" + str(j.if_white())),
            print("***")

        for i in self.stone_list:
            for j in i:
                if j.xx() == x + 1 and j.yy() == y or j.xx() == x - 1 and j.yy() == y or j.xx() == x and j.yy() == y + 1 or j.xx() == x and j.yy() == y - 1:
                    if j.if_white() == s.if_white():
                        flag = True
                        break
            if flag == True and i != self.stone_list[len(self.stone_list) - 1]:
                temp_i = i
                # self.stone_list.remove(i)
                # print("del...")
                # self.stone_list[len(self.stone_list) - 1] = self.stone_list[len(self.stone_list) - 1] + temp_i
                flag = False
                temp_list1 = temp_list1 + i
            else:
                temp_list.append(i)
        temp_list.append(temp_list1)
        temp_list.remove([])

        self.stone_list = [[]]
        ii = 0
        for i in temp_list:
            for j in i:
                self.stone_list[ii].append(j)
            ii = ii + 1
            self.stone_list.append([])
        self.stone_list.remove([])

        if self.isAlive(self.turn) == True and self.isAlive(temp_turn) == False:
            self.stone_list = [[]]
            ii = 0
            for i in origin:
                for j in i:
                    self.stone_list[ii].append(j)
                ii = ii + 1
                self.stone_list.append([])
            self.stone_list.remove([])
            self.stone_list.remove([])
            self.msg = True
            if self.turn == BLACKSTONE:
                self.turn = WHITESTONE
            else:
                self.turn = BLACKSTONE
        else:    
            self.capStones(self.turn)

        # print("new list:")
        # for i in self.stone_list:
        #     for j in i:
        #         print("(" + str(j.xx()) + " ," + str(j.yy()) + ")" + str(j.if_white())),
        #     print("***")

    def showNext(self, x, y):
        # global curser_x
        # global curser_y

        # print("x : " + str(x) + " y : " + str(y))
        # pdb.set_trace()
        if(y < len(self.stone_list[x]) - 1):
            self.curser_y = y + 1
        elif(x < len(self.stone_list) - 1):
            self.curser_x = x + 1
            self.curser_y = 0
        else:
            self.curser_x = 0
            self.curser_y = 0
            self.end = True
        if len(self.stone_list[x]) == 0:
            return None
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

        self.file_name = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
    
    def paintEvent(self, QPaintEvent):
        # global curser_x
        # global curser_y
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
        game_go.resetEnd()
        while not game_go.isEnd():
            self.press_flag = 0
            temp = game_go.showNext(game_go.get_curser_x(), game_go.get_curser_y())
            if temp == None:
                continue
            x = temp.xx() - 1
            y = temp.yy() - 1
            if temp.if_white() == True:
                p.setPen(QPen(Qt.white))
                linearGradient = QLinearGradient(0, 0, 400, 400)
                linearGradient.setColorAt(0.0, Qt.white)
                p.setBrush(linearGradient)
            else:
                p.setPen(QPen(Qt.black))
                linearGradient = QLinearGradient(0, 0, 400, 400)
                linearGradient.setColorAt(0.0, Qt.black)
                p.setBrush(linearGradient)
            rect = QRect(x*BOARDSPACE - BOARDSPACE/2 + BOARDSTART, y*BOARDSPACE - BOARDSPACE/2 + BOARDSTART, 40, 40)
            p.drawPie(rect, 0 * 16, 360 * 16)

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if x < BOARDSTART or x > BOARDEND or y < BOARDSTART or y > BOARDEND:
            return
        game_go.addStone(int((x + BOARDSPACE/2)/BOARDSPACE), int((y + BOARDSPACE/2)/BOARDSPACE))
        # pdb.set_trace()
        fo = open(self.file_name, 'a')
        fo.write("x: " + str(int((x + BOARDSPACE/2)/BOARDSPACE)) + "y: " + str(int((y + BOARDSPACE/2)/BOARDSPACE)) + "\n")
        fo.close()
        if game_go.isMsg() == True:
            QMessageBox.warning(self,
                    "warning",
                    "you cannot place over here！",
                    QMessageBox.Yes)
        self.update()

if __name__=='__main__':
    app = QApplication(sys.argv)
    form = GameBoard()
    form.move(200, 100)
    form.show()
    app.exec_()