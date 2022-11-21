from flask import Flask, render_template
from config import app_config 
from exception import SystemError
from data_preprocessing import preprocessing
# from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys

try:
    obj = app_config()
    mydb = obj.mydb
    cursor = mydb.cursor()
except Exception as e:
    raise SystemError(e, sys)

try:
    data = pd.read_csv(obj.path)
    prep = preprocessing()
    sentence = data['Question'][234]
    predicted_class = prep.preprocessing_data(sentence)
except Exception as e:
    raise SystemError(e, sys)


app = Flask(__name__)

@app.route('/')
def main():
    return render_template("basic.html",Question = sentence, Answer = predicted_class)

if __name__ == "__main__":
    app.run(debug = True)