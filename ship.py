class Ship:
    def __init__(self, name, length,display):
        self.name= name
        self.length = length
        self.lives = length
        self.alive = True
        self.position = ''
        self.display = display
    def return_places(self):
        places = []
        coord = self.position[:2]
        row = (int)(coord[0])
        col = (int)(coord[1])
        direction = self.position[2:3]
        alignment = self.position[3:]

        if direction == 'h' and alignment == 'l':
            #x starts at 0 and goes until length -1
            for x in range(self.length):
                places.append((str)(row) +(str)(( col-x)))
        elif direction == 'h' and alignment == 'r':
            #x starts at 0 and goes until length -1
            for x in range(self.length):
                places.append((str)(row) +(str)(( col+x)))
        if direction == 'v' and alignment == 'u':
            #x starts at 0 and goes until length -1
            for x in range(self.length):
                places.append((str)(( row-x))+(str)(col))
        elif direction == 'v' and alignment == 'd':
            #x starts at 0 and goes until length -1
            for x in range(self.length):
                places.append((str)(( row+x))+(str)(col))  
        return places
    def set_position(self,position):
        self.position = position