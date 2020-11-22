#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:35:01 2020

@author: francescoserraino
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, DecimalField 
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    av_st = FloatField('Daily average screentime in hours',
                                     validators=[DataRequired()])
    av_pickups = FloatField('Average number of times you pick up your phone per day',
                        validators=[DataRequired()])
    av_notification = FloatField('Average number of notifications per day', validators=[DataRequired()])
    most_used1 = StringField('Your number one most used application',
                                     validators=[DataRequired()])
    most_used2 = StringField('Your second most used application',
                                     validators=[DataRequired()])
    most_used3 = StringField('Your third most used application',
                                     validators=[DataRequired()])
    submit = SubmitField('Get your results')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')