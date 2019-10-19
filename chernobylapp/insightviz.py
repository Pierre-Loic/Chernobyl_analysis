import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image

class Viz_video:
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

    def color_word_cloud(self):
        pass

    def image_word_cloud(self, file_name):
        """ Generate a word cloud from an picture of Chernobyl """
        Chernobyl_coloring = np.array(Image.open("D:\__dossier_essais\PyconFR\Chernobyl\Images\Chernobyl_2.png"))
        wc = WordCloud(background_color="white", mask=Chernobyl_coloring, contour_width=1, random_state=42)
        wc.generate_from_frequencies(self.data)
        image_colors = ImageColorGenerator(Chernobyl_coloring)
        plt.figure(figsize=(10,10))
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis('off')
        self.output(file_name)

if __name__=="__main__":
    pass