from apps import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    namaDepan = db.Column(db.String(64), nullable=False)
    namaBelakang = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.String(6))
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'))


