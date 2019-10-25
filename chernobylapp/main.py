#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
import sbttimport as si
import dataprocess as dp
import insightviz as iv
import pandas as pd

package_directory = os.path.dirname(os.path.abspath(__file__))

class Orchestrator:

    def __init__(self, nb=None, lang="fr"):
        self.data_import = si.Data_import(lang=lang, nb=nb)
        self.lang = lang
    
    def run(self, viz="wordcloud", to_file=False):
        """ Run the visualisation """
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        if viz=="wordcloud" or viz=="wordcloud_img" or viz=="wordcloud_color" :
            for df in data:
                sentences = pd.concat([sentences, df["sentence"]], ignore_index=True)
            nlp = dp.Process_NLP(sentences, lang=self.lang)
            wcloud = iv.Viz_wordcloud(nlp.bag_of_words())
            if viz=="wordcloud":
                wcloud.classic_word_cloud()
            elif viz=="wordcloud_img":
                wcloud.image_word_cloud()
            elif viz=="wordcloud_color":
                color_to_words = {
                                    'yellow': ["danger","problem", "caus"],
                                    'green': ["trouv", "aller", "cas"],
                                    'blue': ["accord", "veux"]
                                }
                wcloud.color_word_cloud(color_to_words)
        elif viz=="video":
            full_list = []
            for df in data:
                full_list += self.data_import.split_for_video(df)
            for i, df in enumerate(full_list):
                nlp = dp.Process_NLP(df["sentence"], lang=self.lang)
                wcloud = iv.Viz_wordcloud(nlp.bag_of_words())
                wcloud.classic_word_cloud(file_name=package_directory + "\\temp\\word_cloud_" + str(i) +".png")
        else:
            print("Type of visualisation not detected")

if __name__=="__main__":
    orch = Orchestrator()
    orch.run()