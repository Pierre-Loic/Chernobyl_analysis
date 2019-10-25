#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
from nltk.stem.snowball import FrenchStemmer
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer

class Process_NLP:
    
    def __init__(self, data, lang="fr"):
        self.lang = lang
        self.stop_words = []
        self.data = data
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
        analyzer = CountVectorizer().build_analyzer()
        return (stemmer.stem(w) for w in analyzer(doc))

    def lemma_eng(self, doc):
        """ English Lemmatizer """
        lemma = WordNetLemmatizer()
        analyzer = CountVectorizer().build_analyzer()
        return (lemma.lemmatize(w) for w in analyzer(doc))

    def bag_of_words(self):
        """ Generate bag of words """ 
        if self.lang=="fr":
            vectorizer = CountVectorizer(analyzer=self.stemmer_fr, min_df=4, max_df=15)
        elif self.lang=="eng":
            vectorizer = CountVectorizer(analyzer=self.lemma_eng, min_df=4, max_df=15)
        vec = vectorizer.fit(self.data)
        bag_of_words = vectorizer.transform(self.data)
        sum_words = bag_of_words.sum(axis=0)
        return [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items() if word not in self.stop_words]

    def lda(self):
        """ Use LDA for topic modelling """
        pass

class Cluster:
    pass