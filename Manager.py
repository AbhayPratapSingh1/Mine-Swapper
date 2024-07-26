import numpy as np
import cv2
from Writer.fontManager import Writer
import random
import sys
from Box.box import box
from Pages.StartPage import StartGamePage
from mainGame.MainGame import MainGame
from Pages.ScoreRestartEndPage import ScoreRestartEnd

class PlayGame:
    def __init__(self):
        self.name = "Mine Swaper!"
        self.start_window = StartGamePage(options=["Easy - 3","Medium - 10","Hard - 50"],name =self.name)

    def play_in_loop(self):
        type = self.get_game_type()
        data = self.start_game_window(type)
        next = self.end_response(data)
        if next == "Restart":
            self.play_in_loop()
        else:
            print("thanks for playing!")


    def get_game_type(self):
        return self.start_window.start()
    
    def start_game_window(self,type):
        game_window = MainGame(name= self.name)
        if type == "Easy - 3":
            game_window.setBoard(col=5,row=5, color=(0,200,0), bomb = 3 , gap=1)
        elif type == "Medium - 10":
            game_window.setBoard(col=10,row=10, color=(0,200,0), bomb = 10, gap=1)
        elif type == "Hard - 50":
            game_window.setBoard(col=20,row=20, color=(0,200,0), bomb = 50, gap=1)
        data = game_window.start()
        del game_window
        return data
    def end_response(self,data):
        if len(data) == 2:
            description = data["description"]
            score = data["score"]
            end_window = ScoreRestartEnd(name=self.name, score=score)
            return end_window.start()


       

