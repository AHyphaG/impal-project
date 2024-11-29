from flask import render_template, request,redirect, url_for,flash
from flask_login import login_required, current_user

from apps import db
from apps.pemesanan import blueprint
from apps.authentication.Vehicles import Vehicles
from apps.pemesanan.models import Orders, Montir
from apps.pemesanan.forms import RegisterKendaraanForm 


@blueprint.route('/order-montir', methods=['GET', 'POST'])
@login_required  # Protect this route with the login_required decorator
def order_montir():
    vehicles = Vehicles.query.filter_by(userID_fk=current_user.id).all()
    
    if not vehicles:
        flash("Anda belum memiliki kendaraan, silakan daftarkan kendaraan terlebih dahulu.")
        return redirect(url_for('pemesanan_blueprint.register_kendaraan'))

    if request.method == 'POST':
        selected_vehicle = request.form['vehicle_id']
        # Cari montir berdasarkan kriteria (misal, lokasi)
        montir = Montir.query.filter_by(is_available=True).first()
        
        if montir:
            # Buat pesanan baru
            new_order = Orders(userIdFK=current_user.id, montirIdFK=montir.montirId, vehicleId=selected_vehicle)
            db.session.add(new_order)
            db.session.commit()
            flash("Pesanan berhasil dibuat, montir sedang dalam perjalanan!")
            return redirect(url_for('order_success'))
        else:
            flash("Tidak ada montir yang tersedia saat ini.")
    
    return render_template('pemesanan/order_montir.html', vehicles=vehicles)


@blueprint.route('/register-kendaraan', methods=['GET', 'POST'])
@login_required  # Protect this route with the login_required decorator
def register_kendaraan():
    form = RegisterKendaraanForm()  # Buat instance form
    if form.validate_on_submit():  # Periksa apakah form valid
        new_vehicle = Vehicles(
            jenis=form.jenis.data,
            manufaktur=form.manufaktur.data,
            tipe=form.tipe.data,
            tahunKeluaran=form.tahun.data,
            noPlat=form.noPlat.data,
            userID_fk=current_user.id
        )
        db.session.add(new_vehicle)
        db.session.commit()
        
        flash("Kendaraan berhasil didaftarkan.")
        return redirect(url_for('authentication_blueprint.route_default'))
    
    return render_template('accounts/register_kendaraan.html', form=form)  # Kirim form ke template