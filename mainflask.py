#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:55:48 2020

@author: francescoserraino
"""

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
import pandas as pd
import numpy as np
from scipy import stats 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import scipy.spatial.distance as dist
from scipy.stats import ttest_1samp

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'title': 'Welcome to the course navigator',
        'content': "So you want to join one of IronHack's coding bootcamps but you aren't sure which path to follow. Not to worry, we have developed a tool that can help you to choose what bootcamp to enroll in based on how you spend your time on your phone. Just navigate to the 'Take the Test' page, open your phone's settings to screen time, and enter all the required information. We will help guide you to the right course. You can also click on the links on the right to view the coure main page and find more information"
    }
]

data = pd.read_excel('screen_use.xlsx').transpose()

def new_person(most_used1, most_used2, most_used3, av_st, av_pickups, av_notification):
    data_first = data.loc[['Most used 1','Most used 2','Most used 3', 'Class']]
    data_second = data.loc[['Daily average ST','Daily average pickups','Daily average notifications']].dropna(axis = 1).transpose()
    #data_first[22] = [input('What is your most used app?'),input('What is your second most used app?'),input('What is your third most used app?'),'nnn']
    data_first[22] = [most_used1, most_used2,most_used3,'nnn']
    CountVec = CountVectorizer(ngram_range=(1,1))
    Count_data = CountVec.fit_transform(data_first.apply((lambda x: " ".join(x))))
    cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names())
    data_train = cv_dataframe
    good_cols = [x for x in cv_dataframe if x not in [['data','ux','webdev','nnn']]]
    X_train = cv_dataframe[good_cols]
    D_train = cv_dataframe['data']
    U_train = cv_dataframe['ux']
    W_train = cv_dataframe['webdev']
    
    data_eval_D = cv_dataframe[cv_dataframe['nnn'] == 1]
    model_D = MultinomialNB()
    model_D.fit(X_train,D_train)
    D = pd.DataFrame(model_D.predict_proba(X_train))
    Dval = D[1].to_frame().loc[cv_dataframe[cv_dataframe['nnn'] == 1].index].values[0][0]
    
    data_eval_U = cv_dataframe[cv_dataframe['nnn'] == 1]
    model_U = MultinomialNB()
    model_U.fit(X_train,U_train) 
    U = pd.DataFrame(model_U.predict_proba(X_train))
    Uval = U[1].to_frame().loc[cv_dataframe[cv_dataframe['nnn'] == 1].index].values[0][0]
    
    data_eval_W = cv_dataframe[cv_dataframe['nnn'] == 1]
    model_W = MultinomialNB()
    model_W.fit(X_train,W_train)
    W = pd.DataFrame(model_W.predict_proba(X_train))
    Wval = W[1].to_frame().loc[cv_dataframe[cv_dataframe['nnn'] == 1].index].values[0][0]
    
    
    #new_row = [input('What is the average amount of time you spend on your screen per day in hours?'),input('On avergae, how many times do you pick up your phone per day?'),input('On average how many notifications do you get per day?')]
    new_row = [av_st, av_pickups, av_notification]
    
    
    data_second.loc[len(data_second)+2] = new_row
    probabilities_num = pd.DataFrame(dist.squareform(dist.pdist(data_second)),index=data_second.index, columns=data_second.index)

    
    webdev_prob_l = []
    data_prob_l = []
    ux_prob_l = []
       
    for i in [0,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23]:
        if data.transpose()['Class'][i] == 'webdev':
            webdev_prob_l.append(probabilities_num[i][24])
        elif data.transpose()['Class'][i] == 'data':
            data_prob_l.append(probabilities_num[i][24])
        elif data.transpose()['Class'][i] == 'UX':
            ux_prob_l.append(probabilities_num[i][24])
            
    webdev_prob = ttest_1samp(webdev_prob_l,0).pvalue/2
    data_prob = ttest_1samp(data_prob_l,0).pvalue/2
    ux_prob = ttest_1samp(ux_prob_l,0).pvalue/2
    

    Dtot = Dval*data_prob
    Utot = ux_prob*Uval
    Wtot = webdev_prob*Wval
    
    
    if (Dtot>Utot) & (Dtot>Wtot):
        return 'you should be a data analyst'
    elif (Utot>Dtot) & (Utot > Wtot):
        return 'you should be a UX designer'
    else:
        return 'you should be a web developer'
    


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Based on your answers, {new_person(request.form['most_used1'], request.form['most_used2'], request.form['most_used3'], request.form['av_st'], request.form['av_pickups'], request.form['av_notification'])}", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)





if __name__ == '__main__':
    app.run(debug=True)