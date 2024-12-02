# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db,login_manager
from apps.home import blueprint
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps.home.forms import ProfileForm


@blueprint.route('/index')
@login_required(role="ANY")
def index():

    return render_template('home/index.html', segment='index')


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
@login_required(role="ANY")
def profile():
    user = current_user
    form = ProfileForm()

    if form.validate_on_submit():
        user.namaDepan = form.namaDepan.data
        user.namaBelakang = form.namaBelakang.data
        user.sex = form.sex.data
        user.email = form.email.data
        user.nomorHp = form.phone.data
        
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))

    form.namaDepan.data = user.namaDepan
    form.namaBelakang.data = user.namaBelakang
    form.email.data = user.email
    form.phone.data = user.nomorHp

    return render_template('accounts/profile.html', form=form, user=user)

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