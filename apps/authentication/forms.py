# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,SubmitField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    nomorHp = StringField('Nomor HP',
                        id='no_hp_create',
                        validators=[DataRequired()])
    
class CreateInformation(FlaskForm):
    namaDepan = StringField('Nama Depan',
                            id='nama_depan_create',
                            validators=[DataRequired()])
    namaBelakang = StringField('Nama Belakang',
                            id='nama_belakang_create',
                            validators=[DataRequired()])
    sex = SelectField('Jenis Kelamin', 
                      id= 'jenis_kelamin_create',
                      choices=[('L', 'Male'), ('P', 'Female')], 
                      validators=[DataRequired()])
    submit = SubmitField('Submit')