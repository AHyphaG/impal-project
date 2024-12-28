# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    #Kolom
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    alamat_active = db.Column(db.Integer, db.ForeignKey('alamat.alamatID'), nullable=True)
    nomorHp = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(10),nullable = False)

    # Relasi
    alamat = db.relationship('Alamat', backref='owner', foreign_keys='Alamat.user_id')
    vehicles = db.relationship('Vehicles', backref='owner', lazy=True)
    customer = db.relationship('Customer', backref = 'owner')
    bengkel = db.relationship('Bengkel', backref = 'owner')

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

    def get_id(self):
        return self.id
    def is_active(self):
        return self.is_active
    def activate_user(self):
        self.is_active = True         
    def get_username(self):
        return self.username
    def get_urole(self):
        return self.role
    


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
