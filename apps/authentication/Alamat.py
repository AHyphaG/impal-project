from apps import db

class Alamat(db.Model):
    __tablename__ = 'alamat'
    alamatID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    provinsi = db.Column(db.String(35), nullable=False)
    kabkot = db.Column(db.String(35), nullable=False)
    kecamatan = db.Column(db.String(35))
    kelurahan = db.Column(db.String(35))
    alamat_lengkap = db.Column(db.String(255))
    nama_alamat = db.Column(db.String(15))
    provid = db.Column(db.Integer)
    kabkotid = db.Column(db.Integer)
    kelid = db.Column(db.Integer)
    kecid = db.Column(db.Integer)