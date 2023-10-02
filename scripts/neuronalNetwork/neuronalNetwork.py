import keras 
import pandas as pd
import numpy as np
import nltk
from spacy.lang.es.stop_words import STOP_WORDS

nltk.download('stopwords')

pf = pd.read_json('scripts/generateScores/subjectScores.json', encoding='utf-8')

pf.drop(['email'], axis=1, inplace=True)
