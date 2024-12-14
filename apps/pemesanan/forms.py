from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired

class RegisterKendaraanForm(FlaskForm):
    jenis = StringField('Jenis Kendaraan', validators=[DataRequired()])
    manufaktur = StringField('Manufaktur', validators=[DataRequired()])
    tipe = StringField('Tipe', validators=[DataRequired()])
    tahun = StringField('Tahun Keluaran', validators=[DataRequired()])
    noPlat = StringField('No Plat', validators=[DataRequired()])
    submit = SubmitField('Daftarkan Kendaraan')

class PesanJasaForm(FlaskForm):
    vehicleId = SelectField('Pilih Kendaraan',
                             choices=[],
                             coerce=int,
                             validators=[DataRequired()])
    keluhan = StringField('Keluhan',
                          validators=[DataRequired()])
    submit = SubmitField('Submit')