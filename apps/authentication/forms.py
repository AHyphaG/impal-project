# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,SubmitField
from wtforms.validators import Email, DataRequired
from wtforms import DateField
from wtforms.validators import DataRequired

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
    
    provinsi = SelectField('Provinsi',
                           validators=[DataRequired()],
                           choices=[],
                           render_kw={'id': 'select2-provinsi', 'class': 'form-control'})
    
    kabkot = SelectField('Kabupaten/kota',
                         validators=[DataRequired()],
                         choices=[],
                         render_kw={'id': 'select2-kabupaten', 'class': 'form-control', 'disabled': 'disabled'})
    
    kecamatan = SelectField('Kecamatan',
                            validators=[DataRequired()],
                            choices=[],
                            render_kw={'id': 'select2-kecamatan', 'class': 'form-control', 'disabled': 'disabled'})
    
    kelurahan = SelectField('Kelurahan',
                            validators=[DataRequired()],
                            choices =[],
                            render_kw={'id': 'select2-kelurahan', 'class': 'form-control', 'disabled': 'disabled'})
    
    alamatLengkap = StringField('Alamat Lengkap',
                                validators=[DataRequired()],
                                id='alamatlengkap')
    
    namaAlamat = StringField('Nama Alamat',
                             validators=[DataRequired()],
                             id='namaalamat')
    
    submit = SubmitField('Submit')

class EditAlamat(FlaskForm):  
    provinsi = SelectField('Provinsi',
                           validators=[DataRequired()],
                           choices=[],
                           render_kw={'id': 'select2-provinsi', 'class': 'form-control'})
    
    kabkot = SelectField('Kabupaten/kota',
                         validators=[DataRequired()],
                         choices=[],
                         render_kw={'id': 'select2-kabupaten', 'class': 'form-control'})
    
    kecamatan = SelectField('Kecamatan',
                            validators=[DataRequired()],
                            choices=[],
                            render_kw={'id': 'select2-kecamatan', 'class': 'form-control'})
    
    kelurahan = SelectField('Kelurahan',
                            validators=[DataRequired()],
                            choices =[],
                            render_kw={'id': 'select2-kelurahan', 'class': 'form-control'})
    
    alamatLengkap = StringField('Alamat Lengkap',
                                validators=[DataRequired()],
                                id='alamatlengkap')
    
    namaAlamat = StringField('Nama Alamat',
                             validators=[DataRequired()],
                             id='namaalamat')
    
    # Tombol submit
    submit = SubmitField('Simpan')
class LoginFormBengkel(FlaskForm):
    username = StringField('Username Bengkel',
                            id='username_login',
                            validators=[DataRequired()])
    password = PasswordField('Password',
                                id='pwd_login',
                                validators=[DataRequired()])
    
class CreateBengkelInformation(FlaskForm):
    namaBengkel = StringField('Nama Bengkel',
                            id='namaBengkel_create',
                            validators=[DataRequired()])
    provinsi = SelectField('Provinsi',
                           validators=[DataRequired()],
                           choices=[],
                           render_kw={'id': 'select2-provinsi', 'class': 'form-control'})
    
    kabkot = SelectField('Kabupaten/kota',
                         validators=[DataRequired()],
                         choices=[],
                         render_kw={'id': 'select2-kabupaten', 'class': 'form-control', 'disabled': 'disabled'})
    
    kecamatan = SelectField('Kecamatan',
                            validators=[DataRequired()],
                            choices=[],
                            render_kw={'id': 'select2-kecamatan', 'class': 'form-control', 'disabled': 'disabled'})
    
    kelurahan = SelectField('Kelurahan',
                            validators=[DataRequired()],
                            choices =[],
                            render_kw={'id': 'select2-kelurahan', 'class': 'form-control', 'disabled': 'disabled'})
    
    alamatLengkap = StringField('Alamat Lengkap',
                                validators=[DataRequired()],
                                id='alamatlengkap')
    
    namaAlamat = StringField('Nama Alamat',
                             validators=[DataRequired()],
                             id='namaalamat')

    submit = SubmitField('Submit')

class CreateMontirInformation(FlaskForm):
    firstname = StringField('First Name',
                            id='firstName_create',
                            validators=[DataRequired()])
    lastname = StringField('Last Name',
                            id='lastName_create',
                            validators=[DataRequired()])
    sex = SelectField('Jenis Kelamin', 
                      id= 'jenis_kelamin_create',
                      choices=[('L', 'Male'), ('P', 'Female')], 
                      validators=[DataRequired()])
    tanggalLahir = DateField('Tanggal Lahir',
                             format='%Y-%m-%d',
                             validators=[DataRequired()])
    tempatLahir= StringField('Tempat Lahir',
                                id='tempatLahir_create',
                                validators=[DataRequired()])
    provinsi = SelectField('Provinsi',
                           validators=[DataRequired()],
                           choices=[],
                           render_kw={'id': 'select2-provinsi', 'class': 'form-control'})
    
    kabkot = SelectField('Kabupaten/kota',
                         validators=[DataRequired()],
                         choices=[],
                         render_kw={'id': 'select2-kabupaten', 'class': 'form-control', 'disabled': 'disabled'})
    
    kecamatan = SelectField('Kecamatan',
                            validators=[DataRequired()],
                            choices=[],
                            render_kw={'id': 'select2-kecamatan', 'class': 'form-control', 'disabled': 'disabled'})
    
    kelurahan = SelectField('Kelurahan',
                            validators=[DataRequired()],
                            choices =[],
                            render_kw={'id': 'select2-kelurahan', 'class': 'form-control', 'disabled': 'disabled'})
    
    alamatLengkap = StringField('Alamat Lengkap',
                                validators=[DataRequired()],
                                id='alamatlengkap')
    
    namaAlamat = StringField('Nama Alamat',
                             validators=[DataRequired()],
                             id='namaalamat')

    submit = SubmitField('Submit')