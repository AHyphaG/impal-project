from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,IntegerRangeField, SubmitField, widgets,SelectField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields import DateField
from datetime import datetime
from apps.pemesanan.models import Category

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

class KategoriForm(FlaskForm):
    namaCategory = StringField('Nama Kategori', validators=[DataRequired()])
    deskripsi = StringField('Deskripsi')
    submit = SubmitField('Tambah Kategori')

class ProductForm(FlaskForm):
    namaProduct = StringField('Nama Produk', validators=[DataRequired()])
    hargaPerSatuan = IntegerField('Harga Per Satuan', validators=[DataRequired()])
    stock = IntegerField('Stok', validators=[DataRequired()])
    category = SelectField('Pilih Kategori', coerce=int, validators=[DataRequired()])
    
    def __init__(self, bengkel_id, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.categoryId, category.namaCategory) for category in Category.query.filter_by(bengkel_id_fk=bengkel_id).all()]

