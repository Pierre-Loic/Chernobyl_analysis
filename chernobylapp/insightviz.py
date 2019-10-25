#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

package_directory = os.path.dirname(os.path.abspath(__file__))

class Viz_video:
    """ Create video from wordcloud files """

    def __init__(self):
        pass

    def add_time(self, df):
        """ Add time on the wordcloud image """
        print(df.index[0])
        print(df.index[-1])

    def add_nb(self):
        pass

    def add_indicator(self):
        pass

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
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis('off')
        self.output(file_name)

    def color_word_cloud(self, color_to_words, default_color="grey", file_name=None):
        """ Generate word cloud with meaningful colors """
        # not debug
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