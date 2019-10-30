#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
import sbttimport as si
import dataprocess as dp
import insightviz as iv
import pandas as pd
import cv2
import glob

package_directory = os.path.dirname(os.path.abspath(__file__))

class Orchestrator:

    def __init__(self, nb=1, lang="fr"):
        self.data_import = si.Data_import(lang=lang, nb=nb)
        self.lang = lang
        self.nb = nb
    
    def analyze(self, person):
        """ Analyze with Word2Vec """
        hyperparameters = [
            (40, 5, 2),
            (50, 5, 2),
            (60, 5, 2),
            (70, 5, 2),
            (40, 10, 2),
            (50, 10, 2),
            (60, 10, 2),
            (70, 10, 2),
        ]
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        for df in data:
            sentences = pd.concat([sentences, df["sentence"]], ignore_index=True)
        nlp = dp.Process_NLP(sentences, lang=self.lang)
        for i, (size, window, min_count) in enumerate(hyperparameters):
            wcloud = iv.Viz_wordcloud(nlp.word_2_vec(person, size=size, window=window, min_count=min_count))
            wcloud.classic_word_cloud(file_name=person+str(i)+".png")

    def create_video(self):
        """ Create video of wordcloud """
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        full_list = []
        for df in data:
            full_list += self.data_import.split_for_video(df)
        # Create all the wordcloud images
        for i, df in enumerate(full_list):
            nlp = dp.Process_NLP(df["sentence"], lang=self.lang)
            wcloud = iv.Viz_wordcloud(nlp.bag_of_words())
            wcloud.classic_word_cloud(file_name=package_directory + "\\temp\\word_cloud_" + str(i) +".png")
            # Add progress bar
            video = iv.Viz_video(package_directory + "\\temp\\word_cloud_" + str(i) +".png", df,
                                full_list[-1].index[-1], episode_nb=self.nb)
            video.add_info()
        # Generate the video
        img_array = []
        print(len(glob.glob(package_directory + "\\temp\\*.png")))
        for i in range(len(glob.glob(package_directory + "\\temp\\*.png"))):
            filename = package_directory + "\\temp\\word_cloud_" + str(i) +".png"
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        # Clean the images


    def show_topics(self):
        """ Show main topics """
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        for df in data:
            sentences = pd.concat([sentences, df["sentence"]], ignore_index=True)
        nlp = dp.Process_NLP(sentences, lang=self.lang)
        nlp.lda()

    def run(self, viz="wordcloud", to_file=False):
        """ Run the visualisation """
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        for df in data:
            sentences = pd.concat([sentences, df["sentence"]], ignore_index=True)
        nlp = dp.Process_NLP(sentences, lang=self.lang)
        wcloud = iv.Viz_wordcloud(nlp.bag_of_words())
        if viz=="wordcloud":
            wcloud.classic_word_cloud()
        elif viz=="wordcloud_img":
            wcloud.image_word_cloud(file_name="image.png")
        elif viz=="wordcloud_color":
            color_to_words = {
                                'yellow': ["danger","problem", "caus"],
                                'green': ["trouv", "aller", "cas"],
                                'blue': ["accord", "veux"]
                            }
            wcloud.color_word_cloud(color_to_words)

if __name__=="__main__":
    orch = Orchestrator()
    orch.run()