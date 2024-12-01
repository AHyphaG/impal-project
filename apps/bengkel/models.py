from flask_login import UserMixin
from apps import db
from sqlalchemy.orm import synonym
from apps.authentication.util import hash_pass
class Bengkel(db.Model, UserMixin):
    __tablename__ = 'bengkel'

    namaBengkel = db.Column(db.String(30), nullable=False)
    bengkelId = db.Column(db.Integer, primary_key=True)
    id = synonym('bengkelId')
    lokasi = db.Column(db.String(50))
    noTelp = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return f"<Bengkel {self.namaBengkel}>"
    
