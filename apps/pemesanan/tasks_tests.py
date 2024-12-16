# @shared_task(ignore_result=False, bind=True)
# def test_get_montir(self):
#     try:
#         # Test koneksi dasar
#         result = db.session.execute('SELECT 1').scalar()
#         print("Koneksi database berhasil")
        
#         # Cek tabel montir dengan raw SQL
#         result = db.session.execute('SELECT COUNT(*) FROM montir').scalar()
#         print(f"Jumlah montir (SQL): {result}")
        
#         # Coba ambil semua montir dengan SQLAlchemy
#         montirs = Montir.query.all()
#         print(f"Jumlah montir (SQLAlchemy): {len(montirs)}")
        
#         # Debug print database URL
#         print(f"Database URL: {db.engine.url}")
        
#         montir_list = []
#         for m in montirs:
#             montir_list.append({
#                 "id": m.montirId,
#                 "nama": m.firstname,
#                 "is_available": m.is_available
#             })
        
#         return {
#             "status": "success",
#             "message": f"Berhasil mengambil {len(montirs)} montir",
#             "data": montir_list,
#             "database_url": str(db.engine.url)
#         }
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return {
#             "status": "error",
#             "message": f"Error: {str(e)}",
#             "data": [],
#             "database_url": str(db.engine.url) if db.engine else "No database connection"
#         }

# from sqlalchemy import inspect
# @shared_task(ignore_result=False, bind=True)  # tambahkan bind=True
# def create_order_task(self, user_id, selected_vehicle_id, keluhan, alamat_id):  # tambahkan self
#     start_time = time.time()
#     timeout = 60
#     if not selected_vehicle_id:
#         self.update_state(state='FAILURE')
#         return {
#             "message": "Kendaraan tidak ditemukan.",
#             "montirDapat": None,
#             "kendaraan": None,
#             "bengkel": None
#         }
#     selected_vehicle = Vehicles.query.filter_by(vehicleID=selected_vehicle_id).first()
            
#     if not alamat_id:
#         self.update_state(state='FAILURE')
#         return {
#             "message": "Alamat aktif tidak ditemukan.",
#             "montirDapat": None,
#             "kendaraan": None,
#             "bengkel": None
#         }

#     print("Database URL:", db.engine.url)
    
#     inspector = inspect(db.engine)
#     tables = inspector.get_table_names()
#     print("Available tables:", tables)
#     print("Trying to query montirs...")
#     user_alamat = Alamat.query.filter_by(alamatID=alamat_id).first()
#     while True:
#         db.session.remove()
#         db.session.begin()
#         print("Iterasi")
#         available_montirs = Montir.query.filter_by(is_available=True).all()
#         print(f"Jumlah montir available: {len(available_montirs)}")

        
#         suitable_montirs = []
#         for montir in available_montirs:
#             montir_cek = Users.query.filter_by(id=montir.user_id_fk).first()
#             alamat_search = Alamat.query.filter_by(alamatID=montir_cek.alamat_active).first()
#             if alamat_search.kabkot == user_alamat.kabkot:
#                 suitable_montirs.append(montir)
        
#         if suitable_montirs:
#             selected_montir = suitable_montirs[0]
#             selected_bengkel = Bengkel.query.filter_by(bengkelId=selected_montir.bengkelIdFK).first()
            
#             new_order = Orders(
#                 orderDate=datetime.now(),
#                 userIdFK=user_id,
#                 montirIdFK=selected_montir.montirId,
#                 kendaraan=selected_vehicle_id,
#                 keluhan=keluhan,
#                 lokasi=user_alamat.alamat_lengkap
#             )
#             db.session.add(new_order)
#             db.session.commit()
            
#             selected_montir.is_available = False
#             selected_montir.status = "OTW"
#             db.session.commit()
            
#             self.update_state(state='SUCCESS')
#             return {
#                 "message": f"Pesanan berhasil dibuat untuk montir {selected_montir.firstname}.",
#                 "montirDapat": {
#                     "id": selected_montir.montirId,
#                     "nama": selected_montir.firstname,
#                     "status": selected_montir.status
#                 },
#                 "kendaraan": {
#                     "id": selected_vehicle_id,
#                     "tipe": selected_vehicle.tipe,
#                     "plat_nomor": selected_vehicle.noPlat,
#                     "keluhan": keluhan
#                 },
#                 "bengkel": {
#                     "id": selected_bengkel.bengkelId,
#                     "namaBengkel": selected_bengkel.namaBengkel
#                 }
#             }
#         else:
#             print("ga ada montir")
#             if time.time() - start_time > timeout:
#                 self.update_state(state='FAILURE')
#                 return {
#                     "message": "Tidak ada montir yang tersedia di kecamatan Anda.",
#                     "montirDapat": None,
#                     "kendaraan": None,
#                     "bengkel": None
#                 }
#             self.update_state(state='PENDING')
#             sleep(5)
