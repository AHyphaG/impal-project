from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,IntegerRangeField, SubmitField, widgets
from wtforms.validators import DataRequired, NumberRange


class TambahMontirForm(FlaskForm):
    idMontir = IntegerField('idMontir',
                         id='idMontir_add',
                         validators=[DataRequired()])
    jabatan = StringField('Jabatan',
                            id='jabatan',
                            validators=[DataRequired()])
    gaji = IntegerField('Gaji (Rupiah)',
                        widget = widgets.RangeInput(step=50000),
                        validators=[NumberRange(min=50000, max=10000000)])
    submit = SubmitField('Submit')


