# -- encoding: utf-8 --
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

import requests

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, CreateInformation, LoginFormBengkel, CreateBengkelForm, CreateBengkelInformation, EditAlamat
from apps.authentication.models import Users
from apps.authentication.Alamat import Alamat
from apps.authentication.Customer import Customer
from apps.authentication.Bengkel import Bengkel

from .Vehicles import Vehicles

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    # return redirect(url_for('authentication_blueprint.login'))
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/index')
def index():
    return render_template('home/index.html')

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)#edited

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)#edited
    return redirect(url_for('home_blueprint.index'))



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']

        # Check if the username exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if the email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Create the user
        user = Users(**request.form)
        user.role = "Customer"
        db.session.add(user)
        db.session.commit()

        customer = Customer(
            namaDepan = "init1",
            namaBelakang = "init1",
            sex = "init1",
            user_id_fk = user.id
        )
        db.session.add(customer)
        db.session.commit()

        login_user(user)
        return redirect(url_for('authentication_blueprint.register_information'))

    return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/register_information', methods=['GET', 'POST'])
@login_required(role="ANY")
def register_information():
    form = CreateInformation(request.form)
    user = current_user
    provinsi_choices = [(prov['id'], prov['nama']) for prov in requests.get("https://ibnux.github.io/data-indonesia/provinsi.json").json()]
    form.provinsi.choices = provinsi_choices

    if form.provinsi.data:
        kabupaten_data = requests.get(f"https://ibnux.github.io/data-indonesia/kabupaten/{form.provinsi.data}.json").json()
        form.kabkot.choices = [(kab['id'], kab['nama']) for kab in kabupaten_data]

    if form.kabkot.data:
        kecamatan_data = requests.get(f"https://ibnux.github.io/data-indonesia/kecamatan/{form.kabkot.data}.json").json()
        form.kecamatan.choices = [(kec['id'], kec['nama']) for kec in kecamatan_data]

    if form.kecamatan.data:
        kelurahan_data = requests.get(f"https://ibnux.github.io/data-indonesia/kelurahan/{form.kecamatan.data}.json").json()
        form.kelurahan.choices = [(kel['id'], kel['nama']) for kel in kelurahan_data]

    customer = Customer.query.filter_by(user_id_fk=user.id).first()

    if form.validate_on_submit():
        customer.namaDepan = form.namaDepan.data
        customer.namaBelakang = form.namaBelakang.data
        customer.sex = form.sex.data
        provinsi_name = dict(provinsi_choices).get(form.provinsi.data, "Provinsi tidak diketahui")
        
        kabkot_name = dict([(kab['id'], kab['nama']) for kab in kabupaten_data]).get(form.kabkot.data, "Kab/Kota tidak diketahui")

        kecamatan_name = dict([(kec['id'], kec['nama']) for kec in kecamatan_data]).get(form.kecamatan.data, "Kecamatan tidak diketahui")

        kelurahan_name = dict([(kel['id'], kel['nama']) for kel in kelurahan_data]).get(form.kelurahan.data, "Kelurahan tidak diketahui")

        alamat = Alamat(
            provinsi=provinsi_name,
            kabkot=kabkot_name,
            kecamatan=kecamatan_name,
            kelurahan=kelurahan_name,
            alamat_lengkap=form.alamatLengkap.data,
            nama_alamat=form.namaAlamat.data,
            user_id = user.id,
            provid = form.provinsi.data,
            kabkotid = form.kabkot.data,
            kecid = form.kecamatan.data,
            kelid = form.kelurahan.data
        )
        db.session.add(alamat)
        db.session.commit()
        print('Data alamat berhasil disimpan ke database.\n')
        print(f"Provinsi: {provinsi_name}, Kab/Kota: {kabkot_name}, Kecamatan: {kecamatan_name}, Kelurahan: {kelurahan_name}")
        return redirect(url_for('home_blueprint.index'))
    return render_template('accounts/create-profile.html',form=form)

@blueprint.route('/vehicles')
@login_required(role="Customer")
def vehicles():
    user_vehicles = Vehicles.query.filter_by(userID_fk=current_user.userID).all()
    
    return render_template('accounts/list_vehicles.html', vehicles=user_vehicles,user=current_user)

@blueprint.route('/list-alamat')
@login_required(role="ANY")
def list_alamat():
    user_alamat = Alamat.query.filter_by(user_id=current_user.userID).all()

    return render_template('accounts/list_alamat.html',alamats=user_alamat,user=current_user)

@blueprint.route('/edit-alamat/<int:alamatIDTerpilih>', methods=['GET', 'POST'])
@login_required(role="ANY")
def edit_alamat(alamatIDTerpilih):
    alamat = Alamat.query.get_or_404(alamatIDTerpilih)

    form = EditAlamat(request.form)
    provinsi_choices = [(prov['id'], prov['nama']) for prov in requests.get("https://ibnux.github.io/data-indonesia/provinsi.json").json()]
    form.provinsi.choices = provinsi_choices

    if form.provinsi.data:
        kabupaten_data = requests.get(f"https://ibnux.github.io/data-indonesia/kabupaten/{form.provinsi.data}.json").json()
        form.kabkot.choices = [(kab['id'], kab['nama']) for kab in kabupaten_data]

    if form.kabkot.data:
        kecamatan_data = requests.get(f"https://ibnux.github.io/data-indonesia/kecamatan/{form.kabkot.data}.json").json()
        form.kecamatan.choices = [(kec['id'], kec['nama']) for kec in kecamatan_data]

    if form.kecamatan.data:
        kelurahan_data = requests.get(f"https://ibnux.github.io/data-indonesia/kelurahan/{form.kecamatan.data}.json").json()
        form.kelurahan.choices = [(kel['id'], kel['nama']) for kel in kelurahan_data]

    if form.validate_on_submit():
        provinsi_name = dict(provinsi_choices).get(form.provinsi.data, "Provinsi tidak diketahui")
        
        kabkot_name = dict([(kab['id'], kab['nama']) for kab in kabupaten_data]).get(form.kabkot.data, "Kab/Kota tidak diketahui")

        kecamatan_name = dict([(kec['id'], kec['nama']) for kec in kecamatan_data]).get(form.kecamatan.data, "Kecamatan tidak diketahui")

        kelurahan_name = dict([(kel['id'], kel['nama']) for kel in kelurahan_data]).get(form.kelurahan.data, "Kelurahan tidak diketahui")

        
        alamat.provinsi=provinsi_name,
        alamat.kabkot=kabkot_name,
        alamat.kecamatan=kecamatan_name,
        alamat.kelurahan=kelurahan_name,
        alamat.alamat_lengkap=form.alamatLengkap.data,
        alamat.nama_alamat=form.namaAlamat.data,
        alamat.provid = form.provinsi.data,
        alamat.kabkotid = form.kabkot.data,
        alamat.kecid = form.kecamatan.data,
        alamat.kelid = form.kelurahan.data
        
        db.session.commit()
        print('Data alamat berhasil disimpan ke database.\n')
        print(f"Provinsi: {provinsi_name}, Kab/Kota: {kabkot_name}, Kecamatan: {kecamatan_name}, Kelurahan: {kelurahan_name}")
        return redirect(url_for('home_blueprint.index'))
    return render_template('accounts/edit_alamat.html',form=form,alamatIDTerpilih=alamat.alamatID)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/login-bengkel', methods=['GET', 'POST'])
def loginBengkel():
    login_form = LoginFormBengkel(request.form)  # Form login khusus Bengkel
    if 'login-bengkel' in request.form:  # Trigger saat form login di-submit

        email = request.form['username']  # Ambil input email
        password = request.form['password']  # Ambil input password

        # Cari admin bengkel berdasarkan email
        admin = Bengkel.query.filter_by(email=email).first()

        # Verifikasi password
        if admin and verify_pass(password, admin.password):
            login_user(admin)  # Login sebagai admin bengkel
            return redirect(url_for('bengkel.bengkel'))  # Redirect ke dashboard Bengkel

        # Jika login gagal, tampilkan pesan error
        return render_template(
            'accounts/login_bengkel.html', 
            msg="Email atau password salah!", 
            form=login_form
        )

    # Render halaman login jika request adalah GET
    return render_template('accounts/login_bengkel.html', form=login_form)

@blueprint.route('/register-bengkel', methods=['GET', 'POST'])
def register_bengkel():
    create_bengkel_form = CreateBengkelForm(request.form)

    if 'register' in request.form:
        nama_bengkel = request.form['namaBengkel']
        email = request.form['email']

        # Check if the nama_bengkel exists
        bengkel = Bengkel.query.filter_by(namaBengkel=nama_bengkel).first()
        if bengkel:
            return render_template('accounts/register_bengkel.html',
                                   msg='Nama bengkel sudah terdaftar',
                                   success=False,
                                   form=create_bengkel_form)

        # Check if the email exists
        bengkel = Bengkel.query.filter_by(email=email).first()
        if bengkel:
            return render_template('accounts/register_bengkel.html',
                                   msg='Email sudah terdaftar',
                                   success=False,
                                   form=create_bengkel_form)

        # Create the bengkel account
        bengkel = Bengkel(**request.form)
        db.session.add(bengkel)
        db.session.commit()

        # Log in the newly created bengkel account
        login_user(bengkel)
        return redirect(url_for('authentication_blueprint.register_bengkel_information'))

    return render_template('accounts/register_bengkel.html', form=create_bengkel_form)


@blueprint.route('/register_bengkel_information', methods=['GET', 'POST'])
@login_required(role="ANY")  # Ensure the user is logged in
def register_bengkel_information():
    form = CreateBengkelInformation(request.form)
    bengkel = current_user  # Fetch the current bengkel

    print('Current Bengkel:', bengkel)

    if form.validate_on_submit():
        # Update the bengkel's information
        bengkel.alamat = form.alamat.data
        bengkel.telepon = form.telepon.data
        bengkel.deskripsi = form.deskripsi.data
        
        db.session.commit()
        print('Bengkel information updated successfully.')
        return redirect(url_for('home_blueprint.index'))

    # Debug output for any form validation errors
    print('Form validation errors:', form.errors)
    
    return render_template('accounts/create-bengkel-profile.html', form=form)


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500