from apps import db

class Bengkel(db.Model):
    __tablename__ = 'bengkel'

    namaBengkel = db.Column(db.String(30), nullable=False)
    bengkelId = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relasi
    employee = db.relationship('Montir', backref='bengkel_owner', lazy=True)  # Ubah nama backref
    pending = db.relationship('Pending', backref='bengkel_related', lazy=True)

    def __repr__(self):
        return f"<Bengkel {self.namaBengkel}>"