# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy.orm import synonym
from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    #Kolom
    # id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, primary_key=True)
    id = synonym('userID')
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    namaDepan = db.Column(db.String(64), nullable=False)
    namaBelakang = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.String(6))
    nomorHp = db.Column(db.String(64), nullable=False)

    #Hubungan
    alamat_active = db.Column(db.Integer, db.ForeignKey('alamat.alamatID'), nullable=True)

    # Relasi ke alamat
    alamat = db.relationship('Alamat', backref='owner', foreign_keys='Alamat.user_id')

    # Relasi ke kendaraan
    vehicles = db.relationship('Vehicles', backref='owner', lazy=True)


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
        return str(self.username)
    
class Alamat(db.Model):
    __tablename__ = 'alamat'
    alamatID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    provinsi = db.Column(db.String(35), nullable=False)
    kabkot = db.Column(db.String(35), nullable=False)
    kecamatan = db.Column(db.String(35))
    kelurahan = db.Column(db.String(35))
    alamat_lengkap = db.Column(db.String(255))
    nama_alamat = db.Column(db.String(15))


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
