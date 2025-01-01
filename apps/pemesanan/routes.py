from flask import render_template, request,redirect, url_for,flash,jsonify, send_file
from flask_login import login_required, current_user
import qrcode
import io

from apps import db
from apps.pemesanan import blueprint
from apps.pemesanan.tasks import create_order_task
from apps.authentication.Vehicles import Vehicles
from apps.authentication.Alamat import Alamat
from apps.pemesanan.models import Orders
from time import sleep

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
        selected_vehicle = int(form.vehicleId.data) 
        print("pukimak: ",selected_vehicle)
        keluhan = form.keluhan.data

        # Ambil alamat aktif user
        user_alamat = Alamat.query.filter_by(alamatID=current_user.alamat_active).first()

        if not user_alamat:
            flash("Alamat aktif tidak ditemukan.")
            return redirect(url_for('home_blueprint.profile'))

        # Panggil task Celery untuk membuat pesanan
        task = create_order_task.apply_async(
            args=[current_user.id, selected_vehicle, keluhan, user_alamat.alamatID]
        )

        # Menampilkan status antrian task
        flash("Pesanan sedang diproses, harap tunggu beberapa saat.")
        return redirect(url_for('pemesanan_blueprint.order_status', task_id=task.id))

    return render_template('pemesanan/order_montir.html', vehicles=vehicles, form=form)

@blueprint.route('/check-order-status/<task_id>', methods=['GET'])
@login_required(role="Customer")
def check_order_status(task_id):
    task = create_order_task.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'result': task.result if task.state == 'SUCCESS' else None
    })

@blueprint.route('/order-status/<task_id>', methods=['GET'])
@login_required(role="Customer")
def order_status(task_id):
    task = create_order_task.AsyncResult(task_id)

    # Jika task belum selesai
    if task.state == 'PENDING' or task.state == 'STARTED':
        return render_template('pemesanan/order_matchmaking.html',task_id=task_id)

    # Jika task sudah selesai
    if task.state == 'SUCCESS':
        result = task.result
        
        montir = result.get('montir')
        kendaraan = result.get('kendaraan')
        message = result.get('message')
        bengkel = result.get('bengkel')

        return render_template(
            'pemesanan/order_success.html',
            result=result,
            montir=montir,
            kendaraan=kendaraan,
            message=message,
            bengkel=bengkel
        )

    return "Terjadi kesalahan dalam pemrosesan pesanan."


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
        return redirect(url_for('home_blueprint.customer_index'))
    
    return render_template('accounts/register_kendaraan.html', form=form)  # Kirim form ke template

@blueprint.route('/pembayaran')
@login_required(role="Montir")
def proses_pembayaran():
    order_id = request.args.get('order_id')
    order = Orders.query.get(order_id)
    print("Order-nya: ",order, "Order ID: ",order_id)
    return render_template('pemesanan/pembayaran.html', order=order)


@blueprint.route('/generate-qrcode')
@login_required(role="Montir")
def generate_qrcode():
    try:
        total_harga = request.args.get('total_harga', 0)
        # Format data untuk QR code
        qr_data = f"ID Pembayaran: 12345\nTotal: Rp{total_harga}"
        
        # Buat QR code dengan pengaturan yang lebih spesifik
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Buat gambar QR
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Simpan ke buffer
        buffer = io.BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=False,
            download_name='qrcode.png'
        )
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return "Error generating QR code", 500

