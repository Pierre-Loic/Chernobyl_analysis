#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords
from nltk.stem.snowball import FrenchStemmer
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class Process_NLP:
    
    def __init__(self, data, lang="fr"):
        self.lang = lang
        self.stop_words = []
        self.data = data
        self.vectorizer = None
        self.import_stop_words()

    def import_stop_words(self):
        """ Import stopwords from file """
        if self.lang=="fr":
            filepath = "stopwords\\stop_words_fr.txt"
        elif self.lang=="eng":
            filepath = "stopwords\\stop_words_eng.txt"
        else:
            raise ValueError("The stop words file is missing")
        with open(filepath) as file:
            stop_words = file.readlines()
        self.stop_words = [word.strip("\n") for word in stop_words]

    def stemmer_fr(self, doc):
        """ French stemmer """
        stemmer = FrenchStemmer()
        analyzer = CountVectorizer(stop_words=self.stop_words).build_analyzer()
        return (stemmer.stem(w) for w in analyzer(doc))

    def lemma_eng(self, doc):
        """ English Lemmatizer """
        lemma = WordNetLemmatizer()
        analyzer = CountVectorizer(stop_words=self.stop_words).build_analyzer()
        return (lemma.lemmatize(w) for w in analyzer(doc))

    def bag_of_words(self):
        """ Generate bag of words """ 
        if self.lang=="fr":
            self.vectorizer = CountVectorizer(analyzer=self.stemmer_fr, min_df=4, max_df=15)
        elif self.lang=="eng":
            self.vectorizer = CountVectorizer(analyzer=self.lemma_eng, min_df=4, max_df=15)
        vec = self.vectorizer.fit(self.data)
        bag_of_words = self.vectorizer.transform(self.data)
        sum_words = bag_of_words.sum(axis=0)
        return [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items() if word not in self.stop_words]

    def lda(self):
        """ Use LDA for topic modelling """
        self.bag_of_words()
        processed_docs_tfidf = self.vectorizer.fit_transform(self.data)
        tf_feature_names = self.vectorizer.get_feature_names()
        # Analysis
        keywords = np.array(self.vectorizer.get_feature_names())
        n_words = 10
        no_topics = 1
        for i in range(10):
            no_topics += 1
            topic_keywords = []
            lda = LatentDirichletAllocation(
                n_components=no_topics, 
                max_iter=10, 
                learning_method='online', 
                learning_offset=50.,
                random_state=0).fit(processed_docs_tfidf)
            for topic_weights in lda.components_:
                top_keyword_locs = (-topic_weights).argsort()[:n_words]
                topic_keywords.append(keywords.take(top_keyword_locs))
            df_topic_keywords = pd.DataFrame(topic_keywords)
            df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
            df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
            print(df_topic_keywords)

    def word_2_vec(self, word, size=50, window=5, min_count=2):
        """ Find similarity of a word in the corpus in English """
        if self.lang=="eng":
            data = [simple_preprocess(remove_stopwords(d)) for d in self.data]
            model = Word2Vec(data, size=size, window=window, min_count=min_count, workers=1, seed=42)
            print(f"Word2Vec uses the following parameters : size={size}, window={window} and min_count={min_count}")
            return model.wv.most_similar(positive=word, topn=30)
        else:
            print("This part of the code is only working in English")