import cv2
import numpy as np
from Writer.fontManager import Writer
from Box.box import box


class StartGamePage:
    def __init__(self,name , options, h=640, w=640, border=20 , border_color=(55,55,55), color = (100,100,0)):
        self.writer = Writer()
        self.name = name
        self.h = h
        self.w = w
        self.color = color
        self.border = border
        self.border_color = border_color
        self.pages = None
        self.selected = ""
        self.start_page_setup(options)

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
                return option
    

    def start_page_setup(self, options, gap_x=50, gap_y=100, option_font_size = 30):
        self.page = np.zeros([self.h,self.w,3], np.uint8)
        self.page[:,:] = self.color
        self.option = dict.fromkeys(options)
        self.gap_x = gap_x
        self.gap_y = gap_y
        self.add_heading()
        self.add_mode(option_font_size)

    def add_heading(self):
        self.heading_size = self.w, 110
        heading = self.page[30:110, 0 : self.w]
        heading = self.writer.write(heading, self.name, 40, (50,50,200))
        self.page[30:110, 0 : self.w] = heading

    def add_mode(self,size):
        height = self.h - self.heading_size[1] - (len(self.option) + 1)* self.gap_x 
        width = self.w - self.gap_y * 2
        block_height = height//len(self.option)
        for i, each in enumerate(self.option):
            self.add_box(block_height, width, self.gap_y, self.heading_size[1] + (i+1)*self.gap_x + i*block_height ,(0,100,0),each , size)
            
    def add_box(self, height, width, x,y,color,name, size):
        easy_box = box((x, y),height , width , x, y , color)
        easy_box.image = self.writer.write(easy_box.image, name, size, (0,0,0))
        self.page[easy_box.y:easy_box.y2, easy_box.x:easy_box.x2] = easy_box.image
        self.option[name] = easy_box

    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            for each in self.option :
                if self.option[each].is_pressed((x,y)):
                    self.selected = each

        if event == cv2.EVENT_MOUSEMOVE:
            pass
