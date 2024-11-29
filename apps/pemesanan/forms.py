from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegisterKendaraanForm(FlaskForm):
    jenis = StringField('Jenis Kendaraan', validators=[DataRequired()])
    manufaktur = StringField('Manufaktur', validators=[DataRequired()])
    tipe = StringField('Tipe', validators=[DataRequired()])
    tahun = StringField('Tahun Keluaran', validators=[DataRequired()])
    noPlat = StringField('No Plat', validators=[DataRequired()])
    submit = SubmitField('Daftarkan Kendaraan')