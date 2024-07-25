import cv2
import numpy as np
from Writer.fontManager import Writer
from Box.box import box


class StartGamePage:
    def __init__(self, h=640, w=640, border=20 , border_color=(55,55,55), color = (100,100,0)):
        self.writer = Writer()
        self.name = "Select From the Option"
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
        self.add_mode()

    def add_heading(self):
        heading = self.page[40:90, 0 : self.w]
        heading = self.writer.write(heading, "MINE SWAPPER!", 40, (50,50,200))
        self.page[40:90, 0 : self.w] = heading

    def add_mode(self):
        height = self.h - 100 - 200
        width = self.w - 220
        self.add_box(height//3, width, 100,150,(0,100,0),"Easy - 3")
        self.add_box(height//3, width, 100,200+height//3,(0,100,0),"Medium - 10")
        self.add_box(height//3, width, 100,250+2*(height//3),(0,100,0),"Hard - 50")
    
    def add_box(self, height, width, x,y,color,name):
        easy_box = box((x, y),height , width , x, y , color)
        easy_box.image = self.writer.write(easy_box.image, name, 30, (0,0,0))
        self.page[easy_box.y:easy_box.y2, easy_box.x:easy_box.x2] = easy_box.image
        self.option[name] = easy_box

    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            if self.option["Easy - 3"].is_pressed((x,y)):
                self.selected = "Easy - 3"
            elif self.option["Medium - 10"].is_pressed((x,y)):
                self.selected = "Medium - 10"
            elif self.option["Hard - 50"].is_pressed((x,y)):
                self.selected = "Hard - 50"
            
        if event == cv2.EVENT_MOUSEMOVE:
            pass
