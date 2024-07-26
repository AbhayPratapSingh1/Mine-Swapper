import cv2
import time
import numpy as np
from random import randint
from Writer.fontManager import Writer
from Box.box import box

class MainGame:
    def __init__(self,name, h=640, w=640, border=20 , border_color=(55,55,55)):
        self.name = name

        self.h = h
        self.w = w
        self.border = border
        self.border_color = border_color

        self.writer = Writer()

        self.hover = None
        self.score = None
        self.description = None

        self.close = False

        self.page = np.zeros([self.h,self.w,3], np.uint8)
        cv2.rectangle(self.page,(0,0), (self.w,self.h), border_color, self.border*2)
    
    def start(self):
        self.play_game = True
        while self.play_game:
            cv2.imshow(self.name, self.page)            
            cv2.setMouseCallback(self.name,self.mouse_event_check_handler)
            key = cv2.waitKey(1)
            if key == 13:
                print("exiting the program !!")
                return {"description": "Forced", "score" : self.score}
            elif self.score != None:
                if self.description == "Lose":
                    self.show_bombs()
                
                return {"description": self.description, "score" : self.score}

    
    def setBoard(self,col=5,row=5, color=(0,200,0), gap=1, bomb = 10):
        self.col = col
        self.row = row
        self.color = color 
        self.bombs = bomb
        self.to_open = col * row - self.bombs 
        self.create_boxes(row, col, color, gap)
        self.place_boxes()
        self.place_bombs(self.bombs)
        self.place_box_value()

    def create_boxes(self, size_row, size_col, color, gap):
        self.boxes = np.zeros([size_col,size_row], dtype=box)
        for column in range(size_col):
            for row in range(size_row):
                height = (self.h-2*self.border)//size_row - 2*gap
                width = (self.w-2*self.border)//size_col - 2*gap
                y = self.border + gap + (self.h - 2*self.border)//size_row * row
                x = self.border + gap + (self.w - 2*self.border)//size_col * column
                temp_box = box((column, row), height, width, x, y, color)
                self.boxes[column,row] = temp_box

    def place_boxes(self):
        for i in range(self.boxes.shape[0]):
            for j in range(self.boxes.shape[1]):
                self.page[ self.boxes[i,j].y :self.boxes[i,j].y2 ,  self.boxes[i,j].x :self.boxes[i,j].x2 ] = self.boxes[i,j].image
    
    def place_bombs(self, bombs):
        while bombs != 0:
            x = randint(0,self.boxes.shape[1]-1)
            y = randint(0,self.boxes.shape[0]-1)
            if self.boxes[y,x].value != "":
                continue
            self.boxes[y,x].value = "Bomb"
            bombs -= 1

    def place_box_value(self):
        for cols in range(self.boxes.shape[0]):
            for rows in range(self.boxes.shape[1]):
                if self.boxes[cols,rows].value == "Bomb":
                    continue
                count = 0
                for i in range(3):
                    for j in range(3):
                        if cols-1+i < 0 or rows-1+j < 0 or cols-1+i >= self.boxes.shape[1] or rows-1+j >= self.boxes.shape[0]:
                            continue
                        else:
                            if self.boxes[cols-1+i,rows-1+j].value == "Bomb":
                                count += 1
                if count != 0:
                    self.boxes[cols, rows].value = str(count)
    
    def show_value(self, pos):
        tempBox = self.boxes[pos[0], pos[1]]
        box_value = tempBox.value
        if box_value == "Bomb":
            tempBox.fill_color((50,50,255))
        elif box_value == "":
            tempBox.fill_color((200,200,200))
        else:
            tempBox.fill_color((200-int(box_value)*50,200-int(box_value)*30,255))
        box_image = tempBox.image
        del self.boxes[pos[0], pos[1]].image

        self.boxes[pos[0], pos[1]].image = self.writer.write(box_image,box_value, 10, (0,0,255))
        self.page[tempBox.y:tempBox.y2 , tempBox.x : tempBox.x2] = self.boxes[pos[0], pos[1]].image

    def show_bombs(self,wait = 200):
        for col in range(self.boxes.shape[1]):
            for row in range(self.boxes.shape[0]):
                if self.boxes[row,col].value == "Bomb" and not self.boxes[row,col].open :
                    self.show_value([row,col])
                    cv2.waitKey(wait)
                    cv2.imshow(self.name, self.page)
                    cv2.setMouseCallback(self.name,self.mouse_event_check_handler)
        while not self.close:
            cv2.waitKey(100)




    def merge_box(self, bt, window): 
        try :
            self.image[window][ bt.y : bt.y2, bt.x:bt.x2] = bt.image[:,:]
        except Exception as e:
            print(f"button {bt.pos} is unable to merge due to exception\n:- {e}")
        
    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            if self.description == "Lose":
                self.close = True
            for cols in range(self.boxes.shape[0]):
                for rows in range(self.boxes.shape[1]):
                    if self.boxes[cols,rows].is_pressed([x,y]) and not self.boxes[cols,rows].open :
                        self.boxes[cols,rows].open = True
                        self.show_value([cols,rows])
                        if self.boxes[cols,rows].value == "Bomb":
                            self.score = self.boxes.shape[0] * self.boxes.shape[1] - (self.to_open + self.bombs)
                            self.description = "Lose"
                        else :
                            if self.to_open == 1 :
                                self.boxes[cols,rows].open = True
                                self.show_value([cols,rows])
                                cv2.imshow(self.name, self.page)
                                self.score = self.boxes.shape[0] * self.boxes.shape[1] * 10
                                self.description = "Win"
                            else : self.to_open -= 1
                        
        if event == cv2.EVENT_MOUSEMOVE:
            if x - self.border in range(0, self.w- self.border*2) and y - self.border in range(0, self.h - self.border*2):
                size_of_col = (self.w-self.border*2) // self.col
                size_of_row = (self.h-self.border*2) // self.row
                col = (x - self.border)//size_of_col
                row = (y - self.border)//size_of_row
                if not self.boxes[col,row].open:
                    self.reset_hover()
                    temp_box = self.boxes[col, row]
                    self.hover = temp_box
                    temp_box.fill_color((0,250,0))
                    self.page[temp_box.y : temp_box.y2, temp_box.x:temp_box.x2] = temp_box.image 
            else :
                self.reset_hover()
        if event==cv2.EVENT_LBUTTONUP:
            pass
    
    def reset_hover(self):
        if self.hover == None or self.hover.open:
            return
        self.hover.fill_color(self.color)
        self.page[self.hover.y : self.hover.y2, self.hover.x:self.hover.x2] = self.hover.image
        self.hover = None 
