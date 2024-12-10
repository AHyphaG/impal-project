from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import (
    current_user,
    login_required
)
from apps import db
from apps.montir import blueprint
from apps.authentication.Montir import Montir
from apps.authentication.models import Users
from apps.authentication.Bengkel import Bengkel
from apps.authentication.Alamat import Alamat
from apps.bengkel.Pending import Pending
from apps.montir.forms import MontirProfile

from datetime import datetime

from sqlalchemy import case

def format_to_idr(value):
    return f"Rp {value:,.0f}".replace(",", ".")

@blueprint.route('/menu')
@login_required(role="Montir")
def beranda_montir():
    montir = Montir.query.filter_by(user_id_fk=current_user.id).first()
    return render_template('montir/beranda_montir.html',montir=montir)

@blueprint.route('/berita')
@login_required(role="Montir")
def berita():
    montir = Montir.query.filter_by(user_id_fk=current_user.id).first()
    tawarans = Pending.query.filter_by(montir_id_fk=montir.montirId)
    today = datetime.now().date()
    tawaran_data = [
        {
            'tawaran':tawaran,
            'bengkel':Bengkel.query.filter_by(bengkelId = tawaran.bengkel_id_fk).first(),
            'gajiIDR':format_to_idr(tawaran.gaji),
            'days_left' : (tawaran.deadline - today).days
        }
        for tawaran in tawarans
    ]

    return render_template('montir/berita_montir.html',tawarans=tawaran_data,montir=montir)

@blueprint.route('/tolak/<int:tawaran_id>', methods=['POST'])
@login_required("Montir")
def tolak_tawaran(tawaran_id):
    tawaran = Pending.query.get_or_404(tawaran_id)

    try:
        tawaran.status = "rejected"
        db.session.commit()
        return jsonify({"message": "Tawaran berhasil ditolak",
                        "updated_at": tawaran.updated_at.strftime('%d-%m-%Y')
                        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@blueprint.route('/status-online/<int:user_id>', methods=['POST'])
@login_required(role="Montir")
def update_status_online(user_id):
    try:
        data = request.get_json()
        new_status = data.get('status_online')

        montir = Montir.query.filter_by(user_id_fk=user_id).first()
        if not montir:
            return jsonify({"error": "Montir not found"}), 404

        montir.is_available = new_status
        db.session.commit()

        return jsonify({"message": "Status updated successfully", "status_online": montir.is_available}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@blueprint.route('/status-online/<int:user_id>', methods=['GET'])
@login_required(role="Montir")
def get_status_online(user_id):
    try:
        montir = Montir.query.filter_by(user_id_fk=user_id).first()
        if not montir:
            return jsonify({"error": "Montir not found"}), 404

        return jsonify({"status_online": montir.is_available}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@blueprint.route('/terima/<int:tawaran_id>', methods=['POST'])
@login_required("Montir")
def terima_tawaran(tawaran_id):
    data = request.json
    montir_id = data.get('parameter1')


    try:
        Pending.query.filter(Pending.montir_id_fk == montir_id, Pending.status == 'pending')\
            .update(
                {
                    "status": case(
                        [(Pending.id == tawaran_id, 'accepted')], 
                        else_='rejected'
                    )
                },
                synchronize_session=False
            )
        db.session.commit()
        montir = Montir.query.get_or_404(montir_id)
        pending = Pending.query.get_or_404(tawaran_id)
        
        montir.bengkelIdFK = pending.bengkel_id_fk
        montir.jabatan = pending.jabatan
        montir.gaji = pending.gaji
        db.session.commit()
        print("ASIAP")
        return jsonify({"message": "Tawaran berhasil diproses.",
                        "updated_at": pending.updated_at.strftime('%d-%m-%Y')
                        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@blueprint.route('/profile-montir', methods=['GET', 'POST'])
@login_required("Montir")
def profile_montir():
    form = MontirProfile()
    
    user = Users.query.filter_by(id=current_user.id).first()
    montir = Montir.query.filter_by(user_id_fk=current_user.id).first()
    alamat = Alamat.query.filter_by(user_id = current_user.id).first()

    if form.validate_on_submit():
            montir.firstname = form.namaDepan.data
            montir.lastname = form.namaBelakang.data
            user.email = form.email.data
            user.nomorHp = form.phone.data
            alamat.alamat_lengkap = form.alamat.data
            
            db.session.commit()
            flash("Edit Profil Berhasil","success")
            return redirect(url_for('montir_blueprint.profile_montir'))

    form.namaDepan.data = montir.firstname
    form.namaBelakang.data = montir.lastname
    form.email.data = user.email
    form.phone.data = user.nomorHp
    form.alamat.data = alamat.alamat_lengkap

    return render_template("bengkel/layouts/profile.html", form=form,montir=montir,user=current_user)