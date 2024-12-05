from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required
)
from flask import flash
from apps import db
from apps.bengkel import blueprint
from apps.authentication.Montir import Montir
from apps.authentication.Bengkel import Bengkel
from apps.bengkel.Pending import Pending
from apps.bengkel.forms import TambahMontirForm


@blueprint.route('/dashboard')
@login_required(role="Bengkel")
def dashboard():
    return render_template('bengkel/dashboard.html')

@blueprint.route('/montir')
@login_required(role="Bengkel")
def montir_page():
    montirs = Montir.query.filter_by(bengkelIdFK=current_user.id)
    return render_template('bengkel/montir_page.html', montirs = montirs, segment = 'montir')

@blueprint.route('/tambah-montir', methods = ['GET', 'POST']) 
@login_required(role="Bengkel")
def tambah_montir():
    form = TambahMontirForm()

    if form.validate_on_submit():
        montir = Montir.query.filter_by(montirId=form.idMontir.data).first()
        bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
        if montir and not montir.bengkelIdFK:
            pending = Pending(
                montir_id_fk = montir.montirId,
                bengkel_id_fk = bengkel.bengkelId,
                gaji = form.gaji.data,
                jabatan = form.jabatan.data
            )
            db.session.add(pending)
            db.session.commit()
            flash('Montir berhasil ditambahkan ke dalam daftar pending.', 'success')
            return redirect(url_for('bengkel_blueprint.montir_page'))
        else:
            flash('Montir tidak tersedia untuk direkrut.', 'danger')
            return render_template('bengkel/tambah_montir.html', form = form)

        
    
    return render_template('bengkel/tambah_montir.html', form = form)
