from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField,SubmitField
from wtforms.validators import Email, DataRequired

class ProfileForm(FlaskForm):
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
    sex = SelectField('Jenis Kelamin', 
                      id='jenis_kelamin_create',
                      choices=[('L', 'Male'), ('P', 'Female')], 
                      validators=[DataRequired()])
    submit = SubmitField('Submit')