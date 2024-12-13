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
from apps.authentication.forms import LoginForm, CreateAccountForm, CreateInformation, LoginFormBengkel, CreateBengkelInformation,CreateMontirInformation, EditAlamat
from apps.authentication.models import Users
from apps.authentication.Alamat import Alamat
from apps.authentication.Customer import Customer
from apps.authentication.Bengkel import Bengkel
from apps.authentication.Montir import Montir

from .Vehicles import Vehicles

from apps.authentication.util import *


@blueprint.route('/')
def route_default():
    # return redirect(url_for('authentication_blueprint.login'))
    return redirect(url_for('authentication_blueprint.index'))

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
            return redirect(url_for('home_blueprint.customer_index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)#edited

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)#edited
    return redirect(url_for('home_blueprint.customer_index'))



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
    
    option, is_valid, form = cekFormAlamat(form)

    customer = Customer.query.filter_by(user_id_fk=user.id).first()

    if form.validate_on_submit() and is_valid:
        customer.namaDepan = form.namaDepan.data
        customer.namaBelakang = form.namaBelakang.data
        customer.sex = form.sex.data
        db.session.add(customer)
        db.session.commit()

        save_address_to_db(form,user,option['provinsi'])
        print('Data alamat berhasil disimpan ke database.\n')
        return redirect(url_for('home_blueprint.customer_index'))
    return render_template('accounts/create-profile.html',form=form)

@blueprint.route('/vehicles')
@login_required(role="Customer")
def vehicles():
    user_vehicles = Vehicles.query.filter_by(userID_fk=current_user.id).all()
    
    return render_template('accounts/list_vehicles.html', vehicles=user_vehicles,user=current_user)

@blueprint.route('/list-alamat')
@login_required(role="ANY")
def list_alamat():
    user_alamat = Alamat.query.filter_by(user_id=current_user.id).all()

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
        return redirect(url_for('home_blueprint.customer_index'))
    return render_template('accounts/edit_alamat.html',form=form,alamatIDTerpilih=alamat.alamatID)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/login-bengkel', methods=['GET', 'POST'])
def loginBengkel():
    login_form = LoginFormBengkel(request.form)
    if 'login-bengkel' in request.form:

        username = request.form['username']
        password = request.form['password']

        admin = Users.query.filter_by(username=username).first()

        if admin and verify_pass(password, admin.password):
            login_user(admin)
            return redirect(url_for('bengkel_blueprint.dashboard'))

        return render_template(
            'accounts/login_bengkel.html', 
            msg="Email atau password salah!", 
            form=login_form
        )

    return render_template('accounts/login_bengkel.html', form=login_form)

@blueprint.route('/register-bengkel', methods=['GET', 'POST'])
def register_bengkel():
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']

        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        user = Users(**request.form)
        user.role = "Bengkel"
        db.session.add(user)
        db.session.commit()

        bengkel = Bengkel(
            namaBengkel = "init1",
            user_id_fk = user.id
        )
        db.session.add(bengkel)
        db.session.commit()

        login_user(user)
        return redirect(url_for('authentication_blueprint.register_bengkel_information'))

    return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/register-bengkel-information', methods=['GET', 'POST'])
@login_required(role="Bengkel")
def register_bengkel_information():
    form = CreateBengkelInformation(request.form)
    user = current_user

    option, is_valid, form = cekFormAlamat(form)

    print('Current Bengkel:', user)
    bengkel = Bengkel.query.filter_by(user_id_fk=user.id).first()

    if form.validate_on_submit() and is_valid:
        if not user.alamat:
            bengkel.namaBengkel = form.namaBengkel.data
            db.session.add(bengkel)
            db.session.commit()

            save_address_to_db(form, user, option['provinsi'])
            print('Alamat Bengkel Sudah Ditambahkan.')
            return redirect(url_for('home_blueprint.customer_index'))
        else:
            update_address_in_db(form, user.alamat, option['provinsi'])


    print('Form validation errors:', form.errors)

    return render_template('accounts/create-bengkel-profile.html', form=form, option=option)


@blueprint.route('/login-montir', methods=['GET', 'POST'])
def login_montir():
    login_form = LoginForm(request.form)
    if 'login-montir' in request.form:

        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('montir_blueprint.beranda_montir'))

        return render_template('accounts/login_montir.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login_montir.html',
                               form=login_form)
    
    return render_template('accounts/login_montir.html', form=login_form)

@blueprint.route('/register-montir', methods=['GET', 'POST'])
def register_montir():
    create_account_form = CreateAccountForm(request.form)
    
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register-montir.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register-montir.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        user = Users(**request.form)
        user.role = "Montir"
        db.session.add(user)
        db.session.commit()

        # montir = Montir(
        #     firstName = "init1",
        #     lastName = "init1",
        #     sex = "init1",
        #     tanggalLahir = "init1",
        #     tempatLahir = "init1",
        #     user_id_fk = user.id
        # )
        # # db.session.add(montir)
        # db.session.commit()

        login_user(user)
        return redirect(url_for('authentication_blueprint.register_montir_information'))

    return render_template('accounts/register-montir.html', form=create_account_form)


@blueprint.route('/register-montir-information', methods=['GET', 'POST'])
@login_required(role="Montir")
def register_montir_information():
    form = CreateMontirInformation(request.form)
    user = current_user

    option, is_valid, form = cekFormAlamat(form)

    print('Current Montir:', user)
    
    montir=Montir()
    if form.validate_on_submit() and is_valid:
        if not user.alamat:
            montir.firstname = form.firstname.data
            montir.lastname = form.lastname.data
            montir.sex = form.sex.data
            montir.tanggalLahir = form.tanggalLahir.data
            montir.tempatLahir = form.tempatLahir.data
            montir.is_available = False
            montir.user_id_fk=user.id
            db.session.add(montir)
            db.session.commit()
            save_address_to_db(form,user,option['provinsi'])
            alamat = Alamat.query.filter_by(user_id=current_user.id).first()
            current_user.alamat_active = alamat.alamatID
            db.session.commit()
            
            save_address_to_db(form, user, option['provinsi'])
            print('Alamat Montir Sudah Ditambahkan.')
            return redirect(url_for('montir_blueprint.beranda_montir'))
        else:
            update_address_in_db(form, user.alamat, option['provinsi'])


    print('Form validation errors:', form.errors)

    return render_template('accounts/create-montir-profile.html', form=form, option=option)



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