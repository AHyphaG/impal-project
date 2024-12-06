from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,IntegerRangeField, SubmitField, widgets
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields import DateField
from datetime import datetime

class TambahMontirForm(FlaskForm):
    idMontir = IntegerField('ID Montir',
                         id='idMontir_add',
                         validators=[DataRequired()])
    jabatan = StringField('Jabatan',
                            id='jabatan',
                            validators=[DataRequired()])
    gaji = IntegerField('Gaji (Rupiah)',
                        widget = widgets.RangeInput(step=50000),
                        validators=[NumberRange(min=50000, max=10000000)])
    deadline = DateField('Deadline',
                         format='%Y-%m-%d',
                         validators=[DataRequired()],
                         default=datetime.today)
    submit = SubmitField('Submit')


