win_size = 500

from graphics import*
from Vertex import*
from Edge import*
import math
import copy

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

    def draw(self, path):

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

            if (path == 0):
                ln.setOutline(color_rgb(0, 0, 0))
            else:
                if (self.e_list[i] in path):
                    ln.setOutline(color_rgb(255, 0, 0))
                    ln.setWidth(2)
                else:
                    ln.setOutline(color_rgb(0, 0, 0))
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
        flag_path = [] #flag czy jest w sciezce
        for i in range(len(self.v_list)):
            flag_path.append(0)
        flag_path[v-1] = 1
        lista_krawedzi = [] #lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziem ja sortowac zeby wyłowić najkrotsza sciezke


        for i in range(len(self.e_list)):
            if(self.e_list[i].start == v or self.e_list[i].target == v):
                lista_krawedzi.append(self.e_list[i])
        lista_krawedzi = sorted(lista_krawedzi, key = lambda a: a.value)

        path = [] # sciezka

        print (flag_path)
        for i in range(len(self.v_list)-1):
            while (1):
                if (flag_path[lista_krawedzi[0].start - 1] == 0):
                    flag_path[lista_krawedzi[0].start - 1] = 1
                    v = lista_krawedzi[0].start
                    print(lista_krawedzi[0].start, lista_krawedzi[0].target)
                    path.append(lista_krawedzi[0])
                    lista_krawedzi.pop(0)
                    break
                elif (flag_path[lista_krawedzi[0].target - 1] == 0):
                    flag_path[lista_krawedzi[0].target - 1] = 1
                    v = lista_krawedzi[0].target
                    print (lista_krawedzi[0].start, lista_krawedzi[0].target)
                    path.append(lista_krawedzi[0])
                    lista_krawedzi.pop(0)
                    break
                else:
                    lista_krawedzi.pop(0)

            for i in range(len(self.e_list)):
                if (self.e_list[i].start == v or self.e_list[i].target == v):
                    if (flag_path[self.e_list[i].start - 1] == 1 and flag_path[self.e_list[i].target - 1] == 1):
                        continue
                    lista_krawedzi.append(self.e_list[i])
            lista_krawedzi = sorted(lista_krawedzi, key=lambda a: a.value)
            print(flag_path)

            for i in range(len(path)):
                print(path[i].start)

        #### RYSOWANIE GRAFU Z ZAZNACZONĄ ŚCIEŻKĄ #########
        self.draw(path)
        ########## KONIEC RYSOWANIA GRAFU #############
        return path

    def sPrima(self, v):
        flag_path = []  # flag czy jest w sciezce
        for i in range(len(self.v_list)):
            flag_path.append(0)
        flag_path[v - 1] = 1
        lista_krawedzi = []  # lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziem ja sortowac zeby wyłowić najkrotsza sciezke

        for i in range(len(self.e_list)):
            if (self.e_list[i].start == v):
                lista_krawedzi.append(self.e_list[i])
        lista_krawedzi = sorted(lista_krawedzi, key=lambda a: a.value)

        path = []  # sciezka

        print(flag_path)
        for i in range(len(self.v_list) - 1):
            if len(lista_krawedzi) == 0:
                print("MST niewyznaczalne")
                break
            while (1):
                if (flag_path[lista_krawedzi[0].target - 1] == 0): #jeśli nie da się utworzyć mst, da błąd list index out of range
                    flag_path[lista_krawedzi[0].target - 1] = 1
                    v = lista_krawedzi[0].target
                    print(lista_krawedzi[0].start, lista_krawedzi[0].target)
                    path.append(lista_krawedzi[0])
                    lista_krawedzi.pop(0)
                    break
                else:
                    lista_krawedzi.pop(0)

            for i in range(len(self.e_list)):
                if (self.e_list[i].start == v):
                    if (flag_path[self.e_list[i].target - 1] == 1):
                        continue
                    lista_krawedzi.append(self.e_list[i])
            lista_krawedzi = sorted(lista_krawedzi, key=lambda a: a.value)
            print(flag_path)

            for i in range(len(path)):
                print(path[i].start)

        #### RYSOWANIE GRAFU Z ZAZNACZONĄ ŚCIEŻKĄ #########
        self.draw(path)
        ########## KONIEC RYSOWANIA GRAFU #############
        return path

    def Dijkstra (self, v):
        n = len(self.v_list)  # liczba wierzcholkow
        w = v # wierzcholek poczatkowy
        lista_laczy = []  # lista podajaca ktory wierzcholek jest juz wyliczony
        d = []  # lista informujaca o koszcie drogi do danego wierzcholka od poczatkowego
        p = []  # lista poprzednich wierzcholkow
        path = []  # lista krawedzi wyznaczonych przez algorytm
        for i in range(n):
            lista_laczy.append(0)
            d.append(math.inf)
            p.append(-1)
            path.append(0)
        lista_laczy[v - 1] = 1
        d[v - 1] = 0
        s = v  # wierzcholek startowy

        lista = []  # lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziemy ja sortowac zeby wyłowić najkrotsza sciezke
        for i in range(n - 1):
            for i in range(len(self.e_list)):
                if (self.e_list[i].start == v or self.e_list[i].target == v):
                    if (lista_laczy[self.e_list[i].start - 1] == 1 and lista_laczy[self.e_list[i].target - 1] == 1):
                        continue
                    lista.append(self.e_list[i])
            lista = sorted(lista, key=lambda a: a.value)

            # petla sprawdzajaca droge od wierzcholka v
            for i in range(len(lista)):
                if lista[0].start == v:
                    if d[lista[0].target - 1] > d[lista[0].start - 1] + lista[0].value:
                        d[lista[0].target - 1] = d[lista[0].start - 1] + lista[0].value
                        p[lista[0].target - 1] = lista[0].start
                        path[lista[0].target - 1] = lista[0]
                    lista.pop(0)
                elif lista[0].target == v:
                    if d[lista[0].start - 1] > d[lista[0].target - 1] + lista[0].value:
                        d[lista[0].start - 1] = d[lista[0].target - 1] + lista[0].value
                        p[lista[0].start - 1] = lista[0].target
                        path[lista[0].start - 1] = lista[0]
                    lista.pop(0)
                else:
                    lista.pop(0)
            # petla szukajaca najblizszego wierzcholka jeszcze nie liczonego
            wartosc = math.inf
            for i in range(len(d)):
                if d[i] < wartosc and lista_laczy[i] == 0:
                    wartosc = d[i]
                    v = i + 1
            lista_laczy[v - 1] = 1

        # print(lista_laczy)
        # print(d)
        # print(p)
        # print(s)
        # print(path)

        # szpiedzy = []
        # for i in range(n):
        #     szpiedzy.append(0)
        #
        # for i in range(n):
        #     z=p[i]
        #     while 1:
        #         if z == -1 or z == w:
        #             break
        #         else:
        #             szpiedzy[z - 1] += 1
        #             z = p[z - 1]
        # print (szpiedzy)



        #### RYSOWANIE GRAFU Z ZAZNACZONĄ ŚCIEŻKĄ #########
        self.draw(path)
        ########## KONIEC RYSOWANIA GRAFU #############
        return path

    def lab1(self):
        szpiedzy = []
        for i in range(len(self.v_list)):
            szpiedzy.append(0)
        wieksza=0

        nowa = copy.deepcopy(self.e_list)
        # print(len(nowa))
        maksymalna = []
        lista_najlepszych = []
        for i in range(len(self.e_list)):


            self.e_list = copy.deepcopy(nowa)
            # self.e_list = nowa
            self.e_list.pop(i)
            # print(len(self.e_list))
            # print(len(nowa))
            for q in range(len(self.v_list)):
                szpiedzy[q] = 0
            for x in range(len(self.v_list)):
                v = x + 1
                n = len(self.v_list)  # liczba wierzcholkow
                w = v  # wierzcholek poczatkowy
                lista_laczy = []  # lista podajaca ktory wierzcholek jest juz wyliczony
                d = []  # lista informujaca o koszcie drogi do danego wierzcholka od poczatkowego
                p = []  # lista poprzednich wierzcholkow
                path = []  # lista krawedzi wyznaczonych przez algorytm
                for i in range(n):
                    lista_laczy.append(0)
                    d.append(math.inf)
                    p.append(-1)
                    path.append(0)
                lista_laczy[v - 1] = 1
                d[v - 1] = 0
                s = v  # wierzcholek startowy

                lista = []  # lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziemy ja sortowac zeby wyłowić najkrotsza sciezke
                for i in range(n - 1):
                    for i in range(len(self.e_list)):
                        if (self.e_list[i].start == v or self.e_list[i].target == v):
                            if (lista_laczy[self.e_list[i].start - 1] == 1 and lista_laczy[
                                self.e_list[i].target - 1] == 1):
                                continue
                            lista.append(self.e_list[i])
                    lista = sorted(lista, key=lambda a: a.value)

                    # petla sprawdzajaca droge od wierzcholka v
                    for i in range(len(lista)):
                        if lista[0].start == v:
                            if d[lista[0].target - 1] > d[lista[0].start - 1] + lista[0].value:
                                d[lista[0].target - 1] = d[lista[0].start - 1] + lista[0].value
                                p[lista[0].target - 1] = lista[0].start
                                path[lista[0].target - 1] = lista[0]
                            lista.pop(0)
                        elif lista[0].target == v:
                            if d[lista[0].start - 1] > d[lista[0].target - 1] + lista[0].value:
                                d[lista[0].start - 1] = d[lista[0].target - 1] + lista[0].value
                                p[lista[0].start - 1] = lista[0].target
                                path[lista[0].start - 1] = lista[0]
                            lista.pop(0)
                        else:
                            lista.pop(0)
                    # petla szukajaca najblizszego wierzcholka jeszcze nie liczonego
                    wartosc = math.inf
                    for i in range(len(d)):
                        if d[i] < wartosc and lista_laczy[i] == 0:
                            wartosc = d[i]
                            v = i + 1
                    lista_laczy[v - 1] = 1
                for i in range(n):
                    z = p[i]
                    while 1:
                        if z == -1 or z == w:
                            break
                        else:
                            szpiedzy[z - 1] += 1
                            z = p[z - 1]
                # print(szpiedzy)
            print(szpiedzy.index(max(szpiedzy)) + 1)
            lista_najlepszych.append(szpiedzy.index(max(szpiedzy)) + 1)
            maksymalna.append(max(szpiedzy))
            print (szpiedzy)
            if wieksza < max(szpiedzy):
                wieksza= szpiedzy.index(max(szpiedzy))


        print(maksymalna)
        print(lista_najlepszych[1])
        print(maksymalna.index(max(maksymalna)))

        self.e_list = copy.deepcopy(nowa)
        super = self.e_list[maksymalna.index(max(maksymalna))]
        # self.e_list.pop(maksymalna.index(max(maksymalna)))
        ############################

        win = GraphWin("My Window", win_size, win_size)
        win.setBackground(color_rgb(255, 255, 255))

        for i in range(self.v_num):
            pt = Point(self.translate(self.v_list[i].x), self.translate(self.v_list[i].y))
            cir = Circle(pt, 20)
            if i == lista_najlepszych[1] - 1:
                cir.setFill(color_rgb(200, 0, 0))
            else:
                cir.setFill(color_rgb(0, 0, 200))
            cir.draw(win)
            txt = Text(pt, i + 1)
            txt.setTextColor(color_rgb(255, 255, 100))
            txt.draw(win)

        for i in range(self.e_num):
            pt1 = Point(self.translate(self.v_list[self.e_list[i].start - 1].x),
                        self.translate(self.v_list[self.e_list[i].start - 1].y))
            pt2 = Point(self.translate(self.v_list[self.e_list[i].target - 1].x),
                        self.translate(self.v_list[self.e_list[i].target - 1].y))
            ln = Line(pt1, pt2)

            if (path == 0):
                ln.setOutline(color_rgb(0, 0, 0))
            else:
                if self.e_list[i] == super:
                    ln.setOutline(color_rgb(0, 0, 255))
                    ln.setWidth(2)
                elif (self.e_list[i] in path):
                    ln.setOutline(color_rgb(255, 0, 0))
                    ln.setWidth(2)
                else:
                    ln.setOutline(color_rgb(0, 0, 0))
            ln.draw(win)

        win.getMouse()
        win.close()
        #################################







    def sDijkstra(self, v):
        n = len(self.v_list)  # liczba wierzcholkow
        lista_laczy = []  # lista podajaca ktory wierzcholek jest juz wyliczony
        d = []  # lista informujaca o koszcie drogi do danego wierzcholka od poczatkowego
        p = []  # lista poprzednich wierzcholkow
        path = []  # lista krawedzi wyznaczonych przez algorytm
        for i in range(n):
            lista_laczy.append(0)
            d.append(math.inf)
            p.append(-1)
            path.append(0)
        lista_laczy[v - 1] = 1
        d[v - 1] = 0
        s = v  # wierzcholek startowy

        lista = []  # lista wszystkich krawedzi wychodzacych z vertex-ów należących do path - bedziemy ja sortowac zeby wyłowić najkrotsza sciezke
        for i in range(n - 1):
            for i in range(len(self.e_list)):
                if (self.e_list[i].start == v):  # zmiana : or self.e_list[i].target == v
                    # if (lista_laczy[self.e_list[i].start - 1] == 1 and lista_laczy[self.e_list[i].target - 1] == 1):
                    #     continue
                    lista.append(self.e_list[i])
            lista = sorted(lista, key=lambda a: a.value)

            # petla sprawdzajaca droge od wierzcholka v
            for i in range(len(lista)):
                if lista[0].start == v:
                    if d[lista[0].target - 1] > d[lista[0].start - 1] + lista[0].value:
                        d[lista[0].target - 1] = d[lista[0].start - 1] + lista[0].value
                        p[lista[0].target - 1] = lista[0].start
                        path[lista[0].target - 1] = lista[0]
                    lista.pop(0)
                # elif lista[0].target == v:
                #     if d[lista[0].start - 1] > d[lista[0].target - 1] + lista[0].value:
                #         d[lista[0].start - 1] = d[lista[0].target - 1] + lista[0].value
                #         p[lista[0].start - 1] = lista[0].target
                #         path[lista[0].start - 1] = lista[0]
                #     lista.pop(0)
                else:
                    lista.pop(0)
            # petla szukajaca najblizszego wierzcholka jeszcze nie liczonego
            wartosc = math.inf
            for i in range(len(d)):
                if d[i] < wartosc and lista_laczy[i] == 0:
                    wartosc = d[i]
                    v = i + 1
            lista_laczy[v - 1] = 1

        print(lista_laczy)
        print(d)
        print(p)
        print(s)
        print(path)
        '''
        # Steiner
        niepotrzebne = [2] #niepotrzebne wierzchołki
        licznik = []
        for i in range(len(niepotrzebne)):
            licznik.append(0)
        for k in range(len(niepotrzebne)):
            for i in range(len(path)):
                if path[i] == 0:
                    continue
                if (path[i].start == niepotrzebne[k] or path[i].target == niepotrzebne[k]):
                    licznik[k] += 1
            if licznik[k] > 1:
                path[niepotrzebne[k] - 1] = 0
        '''

        #### RYSOWANIE GRAFU Z ZAZNACZONĄ ŚCIEŻKĄ #########
        self.draw(path)
        ########## KONIEC RYSOWANIA GRAFU #############
        return path

