#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image, ImageDraw, ImageFont

package_directory = os.path.dirname(os.path.abspath(__file__))

class Viz_video:
    """ Create video from wordcloud files """

    def __init__(self, file_name,  df, time_max, episode_nb=1):
        self.file_name = file_name
        self.episode_nb = episode_nb
        self.im = Image.open(file_name)
        self.time_begin = df.index[0]
        self.time_end = df.index[-1]
        self.time_max = time_max


    def get_size(self):
        """ Get the size of the image """
        width, height = self.im.size
        return width, height

    def increase_size(self, increase_height=40):
        """ Increase the size of the image to add a progress bar """
        width, height = self.get_size()
        self.width = width
        self.new_height = height+increase_height
        self.new_img = Image.new("RGB",(width, self.new_height), color = 'black')
        self.new_img.paste(self.im, (0,0))

    def add_info(self):
        """ Add the episode of the serie """
        self.increase_size()
        self.draw = ImageDraw.Draw(self.new_img)
        font = ImageFont.truetype("arial", 14)
        self.draw.text((10, self.new_height-30),"Episode "+ str(self.episode_nb),(255,255,255),font=font)
        self.draw.rectangle(self.calcul_bar(timedelta(0), self.time_max, self.time_max), outline="white")
        self.draw.rectangle(self.calcul_bar(self.time_begin, self.time_end, self.time_max), fill="white")
        self.new_img.save(self.file_name)

    def calcul_bar(self, min_val, max_val, max_abs):
        """ Calculate coordinates for the progress bar """
        min_x = round(0.2*self.width)
        max_x = round(0.95*self.width)
        min_y = self.new_height-30
        max_y = self.new_height-10
        xmin_cal = min_x + (max_x - min_x) * (min_val / max_abs)
        xmax_cal = min_x + (max_x - min_x) * (max_val / max_abs)
        return xmin_cal, min_y, xmax_cal, max_y

class Viz_wordcloud:
    
    def __init__(self, data):
        self.data = {val[0]:val[1] for val in data}

    def output(self, file_name):
        """ Specify the type of output """
        if file_name:
            plt.savefig(file_name)
        else:
            plt.show()

    def classic_word_cloud(self, width=800, height=500, max_font=110, file_name=None):
        """ Create wordcloud from data """
        wordcloud = WordCloud(width=width, height=height,
                      random_state=21, max_font_size=max_font).generate_from_frequencies(self.data)
        plt.figure(figsize=(15, 12))
        plt.imshow(wordcloud, interpolation="bilinear", aspect="auto")
        plt.axis('off')
        self.output(file_name)

    def color_word_cloud(self, color_to_words, default_color="grey", file_name=None):
        """ Generate word cloud with meaningful colors """
        wc = WordCloud(collocations=False).generate_from_frequencies(self.data)
        word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}   
        grouped_color_func = lambda word, font_size, position, orientation,random_state,font_path: word_to_color.get(word, default_color) 
        wc.recolor(color_func=grouped_color_func)
        plt.figure(figsize=(15, 12))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis('off')
        self.output(file_name)

    def image_word_cloud(self, file_name=None):
        """ Generate a word cloud from an picture of Chernobyl """
        Chernobyl_coloring = np.array(Image.open(package_directory + "\\raw_data\\Chernobyl.png"))
        wc = WordCloud(background_color="white", mask=Chernobyl_coloring, contour_width=1, random_state=42)
        wc.generate_from_frequencies(self.data)
        image_colors = ImageColorGenerator(Chernobyl_coloring)
        plt.figure(figsize=(10,10))
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis('off')
        self.output(file_name)

if __name__=="__main__":
    pass