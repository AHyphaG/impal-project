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

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, CreateInformation, LoginFormBengkel, CreateBengkelForm, CreateBengkelInformation
from apps.authentication.models import Users
from apps.bengkel.models import Bengkel
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
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('authentication_blueprint.register_information'))

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/register_information', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def register_information():
    form = CreateInformation(request.form)
    user = current_user  # Fetch the current user

    print('Current User:', user)

    if form.validate_on_submit():
        # Update the user's information
        user.namaDepan = form.namaDepan.data
        user.namaBelakang = form.namaBelakang.data
        user.sex = form.sex.data
        
        db.session.commit()
        print('User information updated successfully.')
        return redirect(url_for('home_blueprint.index'))

    # Debug output for any form validation errors
    print('Form validation errors:', form.errors)
    
    return render_template('accounts/create-profile.html', form=form)

@blueprint.route('/vehicles')
@login_required
def vehicles():
    user_vehicles = Vehicles.query.filter_by(userID_fk=current_user.userID).all()
    
    return render_template('accounts/list_vehicles.html', vehicles=user_vehicles,user=current_user)

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
@login_required  # Ensure the user is logged in
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