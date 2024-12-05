from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required
)
from flask import flash
from apps import db
from apps.montir import blueprint
from apps.authentication.Montir import Montir
from apps.authentication.Bengkel import Bengkel
from apps.bengkel.Pending import Pending
def format_to_idr(value):
    return f"Rp {value:,.0f}".replace(",", ".")
@blueprint.route('/menu')
@login_required(role="Montir")
def beranda_montir():
    return render_template('montir/beranda_montir.html')

@blueprint.route('/berita')
@login_required(role="Montir")
def berita():
    montir = Montir.query.filter_by(user_id_fk=current_user.id).first()
    tawarans = Pending.query.filter_by(montir_id_fk=montir.montirId)

    tawaran_data = [
        {
            'tawaran':tawaran,
            'bengkel':Bengkel.query.filter_by(bengkelId = tawaran.bengkel_id_fk).first(),
            'gajiIDR':format_to_idr(tawaran.gaji)
        }
        for tawaran in tawarans
    ]

    return render_template('montir/berita_montir.html',tawarans=tawaran_data)