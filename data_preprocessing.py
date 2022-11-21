from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from exception import SystemError
import pickle
import sys

class preprocessing():
    def __init__(self):
        try:
            self.model = pickle.load(open('static/model.pkl', 'rb'))
            self.tfv = pickle.load(open('static/tfidvectorizer.pkl', 'rb'))
            self.le = pickle.load(open('static/labelencoder.pkl','rb'))
        except Exception as e:
            raise SystemError(e, sys)

    def clean(self, sentence:str) -> str:
        try:
            lemmetizer = WordNetLemmatizer()
            exp = word_tokenize(sentence.lower())
            return " ".join([lemmetizer.lemmatize(word) for word in exp])
        except Exception as e:
            raise SystemError(e, sys)

    def preprocessing_data(self, sentence:str)->str:
        try:
            self.sentence = sentence
            ques = self.tfv.transform([self.clean(sentence)])
            class_ = self.le.inverse_transform(self.model.predict(ques))
            return class_[0]
        except Exception as e:
            raise SystemError(e, sys)