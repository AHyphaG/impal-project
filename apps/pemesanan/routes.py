from flask import render_template, request,redirect, url_for,flash
from flask_login import login_required, current_user

from apps import db
from apps.pemesanan import blueprint
from apps.authentication.Vehicles import Vehicles
from apps.pemesanan.models import Orders
from apps.authentication.models import Users
from apps.authentication.Montir import Montir
from apps.authentication.Alamat import Alamat

from apps.pemesanan.forms import RegisterKendaraanForm, PesanJasaForm

from datetime import datetime

@blueprint.route('/order-montir', methods=['GET', 'POST'])
@login_required(role="Customer")
def order_montir():
    # Ambil kendaraan milik user yang sedang login
    vehicles = Vehicles.query.filter_by(userID_fk=current_user.id).all()
    
    if not vehicles:
        flash("Anda belum memiliki kendaraan, silakan daftarkan kendaraan terlebih dahulu.")
        return redirect(url_for('pemesanan_blueprint.register_kendaraan'))
    
    form = PesanJasaForm()
    form.vehicleId.choices = [(vehicle.vehicleID, vehicle.tipe) for vehicle in vehicles]

    if request.method == 'POST' and form.validate_on_submit():
        selected_vehicle = form.vehicleId.data
        keluhan = form.keluhan.data

        # Cari montir yang tersedia
        available_montirs = Montir.query.filter_by(is_available=True).all()

        # Ambil alamat aktif user
        user_alamat = Alamat.query.filter_by(alamatID=current_user.alamat_active).first()

        if not user_alamat:
            flash("Alamat aktif tidak ditemukan.")
            return redirect(url_for('home_blueprint.profile'))

        # Filter montir berdasarkan kecamatan yang sama dengan alamat user
        suitable_montirs = []
        for montir in available_montirs:
            montir_cek = Users.query.filter_by(id=montir.user_id_fk).first()
            alamat_search = Alamat.query.filter_by(alamatID=montir_cek.alamat_active).first()
            if alamat_search.kabkot == user_alamat.kabkot:
                suitable_montirs.append(montir)

        if suitable_montirs:
            # Ambil montir pertama yang tersedia
            selected_montir = suitable_montirs[0]
            
            # Buat pesanan baru
            new_order = Orders(
                orderDate = datetime.now(),
                userIdFK=current_user.id,
                montirIdFK=selected_montir.montirId,
                kendaraan=selected_vehicle,
                keluhan=keluhan,
                lokasi = user_alamat.alamat_lengkap
            )
            db.session.add(new_order)
            db.session.commit()

            flash("Pesanan berhasil dibuat, montir sedang dalam perjalanan!")
            return redirect(url_for('order_success'))

        else:
            flash("Tidak ada montir yang tersedia di kecamatan Anda.")

    return render_template('pemesanan/order_montir.html', vehicles=vehicles, form=form)


@blueprint.route('/register-kendaraan', methods=['GET', 'POST'])
@login_required(role="Customer")
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
