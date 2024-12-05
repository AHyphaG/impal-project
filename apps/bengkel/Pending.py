from apps import db
class Pending(db.Model):
    __tablename__ = 'pending'
    id = db.Column(db.Integer, primary_key=True)
    montir_id_fk = db.Column(db.Integer, db.ForeignKey('montir.montirId'), nullable=False)
    bengkel_id_fk = db.Column(db.Integer, db.ForeignKey('bengkel.bengkelId'), nullable=False)
    status = db.Column(db.Enum('pending', 'rejected', 'accepted', name='status_enum'), nullable=False, default='pending')
    gaji = db.Column(db.Integer, nullable = False)
    jabatan = db.Column(db.String(15), nullable = False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relasi dengan Bengkel dan Montir
    montir = db.relationship('Montir', backref='pending_montir', lazy=True)
    bengkel = db.relationship('Bengkel', backref='pending_bengkel', lazy=True)