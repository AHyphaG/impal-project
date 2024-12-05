from apps import db
from datetime import date

class Montir(db.Model):
    __tablename__ = 'montir'

    bengkelIdFK = db.Column(db.Integer,  db.ForeignKey('bengkel.bengkelId'),nullable=True)
    montirId = db.Column(db.Integer, primary_key=True)
    firstName= db.Column(db.String(10))
    lastName= db.Column(db.String(10))
    sex=db.Column(db.String(1))
    tanggalLahir=db.Column(db.Date)
    tempatLahir=db.Column(db.String(15))
    is_available=db.Column(db.String(1))
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'))

    #relasi
    pending = db.relationship('Pending', backref='montir_pending', lazy=True)
    
    # def __repr__(self):
    #     return f"<Bengkel {self.namaBengkel}>"