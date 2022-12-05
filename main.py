from flask import Flask, render_template, request
from config import app_config 
from exception import SystemError
from data_preprocessing import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import sys,os

# Connecting the MySQL Database to FLASK App
# try:
#     obj = app_config()
#     mydb = obj.mydb
#     cursor = mydb.cursor()
# except Exception as e:
#     raise SystemError(e, sys)

# Reading the Data from csv file 
path = os.path.join(os.getcwd(), "static",'BankFAQs.csv')
upath = os.path.join(os.getcwd(), 'static', 'userdata.csv')
try:
    # obj = app_config()
    data = pd.read_csv(path)
    prep = preprocessing()
    x = pd.DataFrame(columns=['First Name', 'Last Name', 'Phone Number', 'Email id'])
    upath = os.path.join(os.getcwd(), 'static', 'userdata.csv')
    x.to_csv(upath, index=False)
    user = pd.read_csv(upath)
except Exception as e:
    raise SystemError(e, sys)


app = Flask(__name__)

@app.route('/')
def main():
    return render_template("basic.html")

@app.route('/confirm')
def confirm():
    try:
        fname = request.args.get('fname')
        lname = request.args.get('lname')
        phone = request.args.get('phone')
        email = request.args.get('email')
        question = request.args.get('question')
        if phone not in user['Phone Number'].values:
            user.loc[len(user.index)+1] = [fname, lname, phone, email]
            user.to_csv(upath, index=False)
        global pred_class
        t_usr, pred_class = prep.preprocessing_data(question)
        global quest_lst 
        quest_lst = data[data['Class']==pred_class]
        global cos_sims
        cos_sims = quest_lst['Question'].map(lambda x: cosine_similarity(prep.tfv.transform([x]), t_usr))
        cos_sims = cos_sims.tolist()
        global ind 
        ind = np.argmax(cos_sims)
        global pred_quest 
        pred_quest = quest_lst['Question'][quest_lst.index[ind]]
        return render_template('confirm.html', Question = pred_quest)
    except Exception as e:
        raise SystemError(e ,sys)

@app.route('/last')
def last():
    ans = request.args.get('choice')
    if ans=='yes':
        global pred_ans
        pred_ans = quest_lst['Answer'][quest_lst.index[ind]]
        return render_template('last.html', prediction = pred_class, Answer= pred_ans)
    elif ans=='no':
        global lst
        lst = [(j,i) for i,j in enumerate(cos_sims)]
        lst.sort(reverse=True)
        global quslst
        quslst = [quest_lst['Question'][quest_lst.index[i[1]]] for i in lst[0:5]]
        return render_template('options.html', ques = quslst)

@app.route('/option')
def option():
    return render_template('option.html')

@app.route('/last2')
def last2():
    global chs
    chs = int(request.args.get('quest'))
    if chs != 6:
        pred_ans = quest_lst['Answer'][quest_lst.index[lst[chs][1]]]
        return render_template('last2.html', prediction=pred_class, Answer = pred_ans)
    else:
        word = "I'm not able to solve this question at this moment. You can call to customer support +88 8888 8888 \U0001F615"
        return render_template('last.html', prediction = pred_class, Answer = word)


if __name__ == "__main__":
    app.run(debug = True)