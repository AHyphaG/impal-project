from apps import db

class Vehicles(db.Model):
    _tablename_ = 'vehicles'
    vehicleID = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(50), nullable=False)
    manufaktur = db.Column(db.String(50), nullable=False)
    tipe = db.Column(db.String(50), nullable=False)
    tahunKeluaran = db.Column(db.String(10), nullable=False)
    noPlat = db.Column(db.String(10), nullable=False)
    userID_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)