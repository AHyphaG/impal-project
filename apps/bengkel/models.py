from flask_login import UserMixin
from apps import db

class Bengkel(db.Model, UserMixin):
    __tablename__ = 'bengkel'

    namaBengkel = db.Column(db.String(30), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    lokasi = db.Column(db.String(50))
    noTelp = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    

    def __repr__(self):
        return f"<Bengkel {self.namaBengkel}>"
    
