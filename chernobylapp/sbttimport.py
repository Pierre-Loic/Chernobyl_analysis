#
# PYCONFR 2019 - PLB - Conférence Chernobyl/NLP
#

import os
import re
import pandas as pd

package_directory = os.path.dirname(os.path.abspath(__file__))

class Data_import:
    """ Import data in .srt format and clean it into a list of Pandas dataframes """

    def __init__(self, lang="fr", nb=None):
        self.lang = lang
        self.nb = nb

    def create_corpus(self):
        """ Create a corpus for all videos """
        corpus = []
        if self.nb is None:
            for i in range(1, 6):
                with open(package_directory + "\\raw_data\\ST_" + str(i) + "_" + self.lang + ".srt") as file:
                    data = file.readlines()
                    data = self.remove_n(data)
                    data = self.clean_data(data)
                    data = self.add_datetime(data)
                    corpus.append(data)
        else:
            with open(package_directory + "\\raw_data\\ST_" + str(self.nb) + "_" + self.lang + ".srt") as file:
                data = file.readlines()
                data = self.remove_n(data)
                data = self.clean_data(data)
                data = self.add_datetime(data)
                corpus.append(data)
        return corpus
    
    def check_srt(self, data):
        """ Check if the data is from a subtitle file or not """
        if isinstance(data, str):
            pattern = r"^.*\d+\\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}.*$"
            if re.match(pattern, data):
                return True
            else:
                return False
        else:
            raise TypeError("You must send a text file")
    
    def remove_n(self, data):
        """ Remove \n in the data """
        return [d.replace("\n", "") for d in data]

    def clean_data(self, data):
        """ Extract data from subtitles """
        dict_data = {
                        "number" : [],
                        "time_begin" : [],
                        "time_end" : [],
                        "sentence" : [],
                        "italic" : [],
                    }
        # Regex patterns
        regex_number = r"^\d+$"
        regex_time = r"^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}).*$"
        regex_sentence = r"^[^0-9]+$"
        regex_italic_open = r"^.*<i>.*$"
        regex_italic_close = r"^.*</i>.*$"
        # Fill the dictionnary
        p = re.compile(regex_number)
        i_open = re.compile(regex_italic_open)
        i_close = re.compile(regex_italic_close)
        regex_sentence_compile = re.compile(regex_sentence)
        number = None
        time_begin = None
        time_end = None
        italic = False
        for elt in data:
            # i open pattern
            if i_open.match(elt):
                italic = True
            # Number pattern
            if p.match(elt):
                number = int(elt)
            # Time pattern
            time_data = re.findall(regex_time, elt)
            if time_data:
                time_begin = time_data[0][0]
                time_end = time_data[0][1]
            if regex_sentence_compile.match(elt):
                dict_data["number"].append(number)
                dict_data["time_begin"].append(time_begin)
                dict_data["time_end"].append(time_end)
                dict_data["sentence"].append(elt.replace("<i>", "").replace("</i>", ""))
                dict_data["italic"].append(italic)
            # i close pattern
            if i_close.match(elt):
                italic = False
        df = pd.DataFrame(dict_data)
        return df

    def add_datetime(self, df):
        """ Create datetime data and add index """
        df["time_begin"] = pd.to_datetime(df["time_begin"])
        df["time_end"] = pd.to_datetime(df["time_end"])
        df["time_delta"] = df["time_end"] - df["time_begin"]
        df["time"] = df["time_end"] - df["time_begin"][0]
        df = df.set_index("time")
        df = df.drop(['time_end'], axis=1)
        df = df.drop(['time_begin'], axis=1)
        return df

    def split_for_video(self, df, time_end_min=10, step_s=10):
        """ Split the dataframe into small dataframe of same duration """
        df_list = []
        time_end = pd.Timedelta(time_end_min*60, unit='s')
        time_begin = pd.Timedelta(0, unit='s')
        delta_t = pd.Timedelta(step_s, unit='s')
        while not(all(df.index < time_end)):
            temp = df[df.index < time_end]
            result = temp[temp.index > time_begin]
            time_end += delta_t
            time_begin += delta_t
            df_list.append(result)
        return df_list

if __name__=="__main__":
    data = Data_import(nb=1, lang="eng")
    data.split_for_video(data.create_corpus()[0])