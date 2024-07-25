import cv2
import numpy as np
from Writer.fontManager import Writer
from Box.box import box

class ScoreRestartEnd:
    def __init__(self, h=640, w=640, border=20 , border_color=(55,55,55), color = (100,100,0), name = "Game Over!",score=0):
        self.writer = Writer()
        self.name = name
        self.score = score

        self.h = h
        self.w = w
        self.color = color
        self.border = border
        self.border_color = border_color
        self.pages = None
        self.start_page_setup()
        self.selected = ""

    def start(self):
        while True:
            cv2.imshow(self.name, self.page)
            cv2.setMouseCallback(self.name,self.mouse_event_check_handler)
            key = cv2.waitKey(1)
            if key == 13:
                ("exiting the program !!")
                break
            if self.selected != "":
                option = self.selected
                self.selected = ""
                cv2.destroyAllWindows()
                return option
    

    def start_page_setup(self):
        self.page = np.zeros([self.h,self.w,3], np.uint8)
        self.page[:,:] = self.color

        self.option = {}
        self.add_heading()
        self.add_score()
        self.add_mode()

    def add_heading(self):
        heading = self.page[40:90, 0 : self.w]
        heading = self.writer.write(heading, self.name, 32, (50,50,200))
        self.page[40:90, 0 : self.w] = heading

    def add_score(self):
        heading = self.page[120:170, 0 : self.w]
        heading = self.writer.write(heading, "SCORE : "+str(self.score), 40, (50,50,200))
        self.page[120:170, 0 : self.w] = heading

    def add_mode(self):
        height = self.h - 380
        width = self.w - 220
        self.add_box(height//2, width, 100,230,(0,100,0),"Restart")
        self.add_box(height//2, width, 100,280+height//2,(0,100,0),"Exit")
    
    def add_box(self, height, width, x,y,color,name):
        option_box = box((x, y),height , width , x, y , color)
        option_box.image = self.writer.write(option_box.image, name, 30, (0,0,0))
        self.page[option_box.y:option_box.y2, option_box.x:option_box.x2] = option_box.image
        self.option[name] = option_box

    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            if self.option["Restart"].is_pressed((x,y)):
                self.selected = "Restart"
            elif self.option["Exit"].is_pressed((x,y)):
                self.selected = "Exit"
            
        if event == cv2.EVENT_MOUSEMOVE:
            pass
