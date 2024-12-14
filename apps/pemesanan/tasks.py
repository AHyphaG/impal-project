from apps import db
from datetime import datetime
from apps.authentication.Vehicles import Vehicles
from apps.pemesanan.models import Orders
from apps.authentication.models import Users
from apps.authentication.Montir import Montir
from apps.authentication.Alamat import Alamat
from apps.authentication.Bengkel import Bengkel
from celery import shared_task
from time import sleep
import time


@shared_task(ignore_result=False)
def create_order_task(user_id, selected_vehicle_id, keluhan, alamat_id):
    start_time = time.time()
    timeout = 60

    while True:
        print("TEST")
        selected_vehicle = Vehicles.query.filter_by(vehicleID=selected_vehicle_id).first()

        if not selected_vehicle:
            return "Kendaraan tidak ditemukan."

        available_montirs = Montir.query.filter_by(is_available=True).all()

        # Ambil alamat aktif user
        user_alamat = Alamat.query.filter_by(alamatID=alamat_id).first()

        if not user_alamat:
            return "Alamat aktif tidak ditemukan."

        suitable_montirs = []
        for montir in available_montirs:
            montir_cek = Users.query.filter_by(id=montir.user_id_fk).first()
            alamat_search = Alamat.query.filter_by(alamatID=montir_cek.alamat_active).first()
            if alamat_search.kabkot == user_alamat.kabkot:
                suitable_montirs.append(montir)
                print("masuk montir")
        if suitable_montirs:
            # Ambil montir pertama yang tersedia
            selected_montir = suitable_montirs[0]
            selected_bengkel = Bengkel.query.filter_by(bengkelId=selected_montir.bengkelIdFK).first()
            # Buat pesanan baru
            new_order = Orders(
                orderDate=datetime.now(),
                userIdFK=user_id,
                montirIdFK=selected_montir.montirId,
                kendaraan=selected_vehicle.vehicleID,
                keluhan=keluhan,
                lokasi=user_alamat.alamat_lengkap
            )
            db.session.add(new_order)
            db.session.commit()

            selected_montir.is_available = False
            selected_montir.status = "OTW"
            db.session.commit()

            return {
                "message": f"Pesanan berhasil dibuat untuk montir {selected_montir.firstname}.",
                "montir": {
                    "id": selected_montir.montirId,
                    "nama": selected_montir.firstname,
                    "status": selected_montir.status
                },
                "kendaraan": {
                    "id": selected_vehicle.vehicleID,
                    "tipe": selected_vehicle.tipe,
                    "plat_nomor": selected_vehicle.noPlat,
                    "keluhan":keluhan
                },
                "bengkel":{
                    "id":selected_bengkel.bengkelId,
                    "namaBengkel":selected_bengkel.namaBengkel
                }
            }
        else:
            print("ga ada montir")
        if time.time() - start_time > timeout:
            return {
                "message": "Tidak ada montir yang tersedia di kecamatan Anda.",
                "montir": None
            }
        
        sleep(5)

