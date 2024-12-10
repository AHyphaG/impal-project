from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,SubmitField
from wtforms.validators import Email, DataRequired
from wtforms.validators import DataRequired

class MontirProfile(FlaskForm):
    namaDepan = StringField('Nama Depan',
                            id='nama_depan_create',
                            validators=[DataRequired()])
    namaBelakang = StringField('Nama Belakang',
                            id='nama_belakang_create',
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Nomor Telepon',
                        validators=[DataRequired()])
    alamat = StringField('Alamat',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')