import sys
import numpy as np
from PIL import ImageFont, Image, ImageDraw


class Writer:
    textDimension = lambda self, text_box : [text_box[2] - text_box[0], text_box[3] - text_box[1]]    
    def __init__(self):
        self.font = None
        self.position = [0, 0]
        self.Lines = []
        self.path = "./Writer/testFont.ttf"

    def loadFont(self, size):
        try:
            font = ImageFont.truetype(self.path, size)
        except IOError:
            print(f"Font at location {self.path} doesn't found please place font there!")
            sys.exit(1)
        self.font = font
    
    def normalisePosition(self , font_box):
        position = [0,0]
        position[0] -= font_box[0]
        position[1] -= font_box[1]
        self.position = position

    def setTextBoxAndPosition(self , text, size):
        textBox = self.font.getbbox(text) # this is for getting cordinates of the box if the position taken is (0,0) [x0,y0,x1,y1]
        textSize = self.textDimension(textBox) # determininge the size of the bredth and the height of the text in the fonts
        self.normalisePosition(textBox) # normalising the position as per the text box x0,y0 cordinates so position given should be match
        
        self.position[0] = size[0]//2
        self.position[1] = size[1]//2
        self.position[0] = self.position[0] - textSize[0]//2
        self.position[1] = self.position[1] - textSize[1]

    def write(self, image, text, fontSize=10, color=(0,0,0) ):

        self.loadFont(fontSize)

        self.setTextBoxAndPosition(text, size=image.shape[:2][::-1])
        
        # convert np array to pil image
        image_pil = Image.fromarray(image)
        # create the image drawer for the image
        draw = ImageDraw.Draw(image_pil)
        # writing the text in the images
        draw.text(self.position, text, font=self.font, fill=color)
        # Convert PIL image back to Numpy image
        image_with_text = np.array(image_pil)
        return image_with_text
