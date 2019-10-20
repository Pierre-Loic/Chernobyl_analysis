import sbttimport as si
import dataprocess as dp
import insightviz as iv
import pandas as pd

class Orchestrator:

    def __init__(self, nb=None, lang="fr"):
        self.data_import = si.Data_import(lang=lang, nb=nb)
        self.lang = lang
    
    def run(self, viz="wordcloud", to_file=False):
        sentences = pd.Series()
        data = self.data_import.create_corpus()
        if viz=="wordcloud" or viz=="wordcloud_img":
            for df in data:
                sentences = pd.concat([sentences, df["sentence"]], ignore_index=True)
            nlp = dp.Process_NLP(sentences, lang=self.lang)
            wcloud = iv.Viz_wordcloud(nlp.bag_of_words())
            if viz=="wordcloud":
                wcloud.classic_word_cloud()
            elif viz=="wordcloud_img":
                wcloud.image_word_cloud()
        else:
            pass

if __name__=="__main__":
    orch = Orchestrator()
    orch.run()