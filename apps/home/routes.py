# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db,login_manager
from apps.home import blueprint
from flask import render_template, redirect, request, url_for, jsonify, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps.authentication.Alamat import Alamat
from apps.authentication.Bengkel import Bengkel
from apps.pemesanan.models import Product

from apps.home.forms import ProfileForm, TambahAlamat
from apps.authentication.Customer import Customer

from apps.authentication.util import *

@blueprint.route('/index')
@login_required(role="Customer")
def index():
    redirect(url_for('home_blueprint.customer_index'))




@blueprint.route('/customer')
@login_required(role="Customer")
def customer_index():
    customer = Customer.query.filter_by(user_id_fk=current_user.id)

    return render_template('home/customer.html',customer=customer)

@blueprint.route('/<template>')
@login_required(role="ANY")
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
    
@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required(role="Customer")
def profile():
    user = current_user
    customer = Customer.query.filter_by(user_id_fk=user.id).first()
    form = ProfileForm()

    if form.validate_on_submit():
        customer.namaDepan = form.namaDepan.data
        customer.namaBelakang = form.namaBelakang.data
        customer.sex = form.sex.data
        user.email = form.email.data
        user.nomorHp = form.phone.data
        
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))

    form.namaDepan.data = customer.namaDepan
    form.namaBelakang.data = customer.namaBelakang
    form.email.data = user.email
    form.phone.data = user.nomorHp

    return render_template('accounts/profile.html', form=form, user=user)


@blueprint.route('/search', methods=['GET'])
@login_required(role="Customer")
def search():
    search_type = request.args.get('type')
    query = request.args.get('query')

    if search_type == 'bengkel':
        results = Bengkel.query.filter(Bengkel.namaBengkel.ilike(f"%{query}%")).all()
    elif search_type == 'produk':
        results = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        return jsonify({"error": "Invalid search type"}), 400

    # Format response data
    response_data = []
    for result in results:
        if search_type == 'bengkel':
            response_data.append({
                "id": result.bengkelId,
                "name": result.namaBengkel
            })
        elif search_type == 'produk':
            response_data.append({
                "id": result.id,
                "name": result.name,
                "description": result.description,
                "price": result.price
            })

    return jsonify({"results": response_data})


@blueprint.route('/tambah_alamat', methods=['GET', 'POST'])
@login_required(role="Customer")
def tambah_alamat():
    form =TambahAlamat(request.form)
    user = current_user
    
    option, is_valid, form = cekFormAlamat(form)

    customer = Customer.query.filter_by(user_id_fk=user.id).first()

    if form.validate_on_submit() and is_valid:
        save_address_to_db(form,user,option['provinsi'])
        print('Data alamat berhasil disimpan ke database.\n')
        return redirect(url_for('home_blueprint.customer_index'))
    return render_template('accounts/edit_alamat.html',form=form)

@blueprint.route('/pilih-alamat/<int:alamatIDTerpilih>', methods=['GET', 'POST'])
@login_required(role="Customer")
def pilih_alamat(alamatIDTerpilih):
    user = current_user
    user.alamat_active = alamatIDTerpilih
    db.session.commit()
    flash("Alamat berhasil dipilih")
    return redirect(url_for('authentication_blueprint.list_alamat'))

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