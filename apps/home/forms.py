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

class TambahAlamat(FlaskForm):
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