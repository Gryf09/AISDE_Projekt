class Edge():
    def __init__(self, ID, start, target):
        self.ID = ID
        self.start = start
        self.target = target
    def show(self):
        print(self.ID, self.start, self.target)