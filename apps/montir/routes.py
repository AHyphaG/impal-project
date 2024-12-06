from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import (
    current_user,
    login_required
)
from apps import db
from apps.montir import blueprint
from apps.authentication.Montir import Montir
from apps.authentication.Bengkel import Bengkel
from apps.bengkel.Pending import Pending

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