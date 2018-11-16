win_size = 500

from graphics import*
from Vertex import*
from Edge import*
import math

class Network():

    v_list = [] #lista wezlow
    e_list = [] #lista laczy

    def __init__(self):
        x = 0
        y = 0
        ID = 0
        start = 0
        target = 0
        flag = "0"

        f = open("network.txt", 'r')
        for line in f:
            if line[0] != '#':
                if 'WEZLY' in line:
                    for word in line.split():  # word zostaje ostatnim slowem, czyli tym co jest po =
                        liczba_wezlow = word
                        flag = "w"
                    continue
                if 'LACZA' in line:
                    for word in line.split():
                        liczba_laczy = word
                        flag = "l"
                    continue
                if flag == "w":
                    for counter, word in enumerate(line.split()):
                        if counter == 0:
                            ID = int(word)
                        elif counter == 1:
                            x = int(word)
                        elif counter == 2:
                            y = int(word)
                    self.add_Vertex(ID, x, y)
                elif flag == "l":
                    for counter, word in enumerate(line.split()):
                        if counter == 0:
                            ID = int(word)
                        elif counter == 1:
                            start = int(word)
                        elif counter == 2:
                            target = int(word)
                    self.add_Edge(ID, start, target)

        self.v_num = int(liczba_wezlow)
        self.e_num = int(liczba_laczy)

        for i in range(self.e_num):
            x1 = self.v_list[self.e_list[i].start - 1].x
            x2 = self.v_list[self.e_list[i].target - 1].x
            y1 = self.v_list[self.e_list[i].start - 1].y
            y2 = self.v_list[self.e_list[i].target - 1].y
            self.e_list[i].value = round(float(math.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )),2)

    def add_Vertex(self,ID, x, y):
        self.v_list.append(Vertex(ID, x, y))

    def add_Edge(self,ID, start, target):
        self.e_list.append(Edge(ID, start, target))

    def translate(self, value):
        # Figure out how 'wide' each range is
        fromSpan = 110 - 0
        toSpan = win_size - 0

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - 0) / float(fromSpan)

        # Convert the 0-1 range into a value in the right range.
        return 0 + (valueScaled * toSpan)

    def draw(self):

        win = GraphWin("My Window", win_size, win_size)
        win.setBackground(color_rgb(255, 255, 255))


        for i in range(self.v_num):
            pt = Point(self.translate(self.v_list[i].x), self.translate(self.v_list[i].y))
            cir = Circle(pt, 20)
            cir.setFill(color_rgb(0, 0, 200))
            cir.draw(win)
            txt = Text(pt,i+1)
            txt.setTextColor(color_rgb(255,255,100))
            txt.draw(win)

        for i in range(self.e_num):
            pt1 = Point(self.translate(self.v_list[self.e_list[i].start - 1].x), self.translate(self.v_list[self.e_list[i].start - 1].y))
            pt2 = Point(self.translate(self.v_list[self.e_list[i].target - 1].x), self.translate(self.v_list[self.e_list[i].target - 1].y))
            ln = Line(pt1, pt2)
            ln.setOutline(color_rgb(0,0,0))
            ln.draw(win)

        win.getMouse()
        win.close()

    def show(self):
        for i in range(self.v_num):
            self.v_list[i].show()
        print("")
        for i in range(self.e_num):
            self.e_list[i].show()

    def Prima(self, v):
        lista_laczy = [] #flag czy jest w dżewie
        for i in range(len(self.v_list)):
            lista_laczy.append(0)
        lista_laczy[v-1] = 1
        lista = [] #lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziem ja sortowac zeby wyłowić najkrotsza sciezke
        for i in range(len(self.e_list)):
            if(self.e_list[i].start == v or self.e_list[i].target == v):
                lista.append(self.e_list[i])
        lista = sorted(lista, key = lambda a: a.value)
        #print(lista[1].ID)
        #lista.extend(sorted(self.e_list, key = lambda a: a.value))
        #min_value = 0
        path = [] #drzewo
        path.append(lista[0])
        print(lista)
        while(1):
            if(lista_laczy[lista[0].start-1] == 0):
                lista_laczy[lista[0].start-1] = 1
                v = lista[0].start
                lista.pop(0)
                break
            elif(lista_laczy[lista[0].target-1] == 0):
                lista_laczy[lista[0].target - 1] = 1
                v = lista[0].target
                lista.pop(0)
                break
            else:
                lista.pop(0)

        for i in range(len(self.e_list)):
            if(self.e_list[i].start == v or self.e_list[i].target == v):
                if (lista_laczy[self.e_list[i].start-1] == 1 and lista_laczy[self.e_list[i].target-1]==1):
                    continue
                lista.append(self.e_list[i])
        lista = sorted(lista, key=lambda a: a.value)
        print(lista)

        #for i in range(len(self.v_list)-1):
          #  lista.extend()
            #print(lista[0].ID)



        return path