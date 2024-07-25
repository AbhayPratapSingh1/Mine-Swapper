import numpy as np
class box:
    def __init__(self, pos, h, w, x, y, color=[0,0,0]):
        self.h = h
        self.w = w
        self.x = x
        self.y = y
        self.x2 = x + w
        self.y2 = y + h

        self.pos = pos
        
        self.color = color
        self.image = None

        self.open = False
        self.value = ""
        self.create()

    def create(self):
        self.image = np.zeros([self.h,self.w,3],dtype=np.uint8)
        self.fill_color(self.color)
        self.rawImage = self.image.copy()


    def fill_color(self,color):
        self.image[:,:] = color
    
    def is_pressed(self,pos):
            if pos[0] >= self.x and pos[0] < self.x2 and pos[1] >= self.y and pos[1] < self.y2:
                return True
            return False
    def action(self):
        obj = {"type": "input","value":"text"}
        return obj
