win_size = 500

from graphics import*
from Vertex import*
from Edge import*

class Network():

    v_list = []
    e_list = []

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
        pt = []

        for i in range(self.v_num):
            pt = Point(self.translate(self.v_list[i].x), self.translate(self.v_list[i].y))
            cir = Circle(pt, 10)
            cir.setFill(color_rgb(0, 0, 100))
            cir.draw(win)

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