# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import hashlib
import binascii

from apps import db
from apps.authentication.Alamat import Alamat

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/


def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


import requests

# Mengambil data dari API
def get_provinsi_choices():
    return [(prov['id'], prov['nama']) for prov in requests.get("https://ibnux.github.io/data-indonesia/provinsi.json").json()]

def get_kabupaten_choices(provinsi_id):
    return [(kab['id'], kab['nama']) for kab in requests.get(f"https://ibnux.github.io/data-indonesia/kabupaten/{provinsi_id}.json").json()]

def get_kecamatan_choices(kabkot_id):
    return [(kec['id'], kec['nama']) for kec in requests.get(f"https://ibnux.github.io/data-indonesia/kecamatan/{kabkot_id}.json").json()]

def get_kelurahan_choices(kecamatan_id):
    return [(kel['id'], kel['nama']) for kel in requests.get(f"https://ibnux.github.io/data-indonesia/kelurahan/{kecamatan_id}.json").json()]

def save_address_to_db(form, user, provinsi_choices):
    provinsi_name = dict(provinsi_choices).get(form.provinsi.data, "Provinsi tidak diketahui")
    kabkot_name = dict(get_kabupaten_choices(form.provinsi.data)).get(form.kabkot.data, "Kab/Kota tidak diketahui")
    kecamatan_name = dict(get_kecamatan_choices(form.kabkot.data)).get(form.kecamatan.data, "Kecamatan tidak diketahui")
    kelurahan_name = dict(get_kelurahan_choices(form.kecamatan.data)).get(form.kelurahan.data, "Kelurahan tidak diketahui")
    
    alamat = Alamat(
        provinsi=provinsi_name,
        kabkot=kabkot_name,
        kecamatan=kecamatan_name,
        kelurahan=kelurahan_name,
        alamat_lengkap=form.alamatLengkap.data,
        nama_alamat=form.namaAlamat.data,
        user_id=user.id,
        provid=form.provinsi.data,
        kabkotid=form.kabkot.data,
        kecid=form.kecamatan.data,
        kelid=form.kelurahan.data
    )
    
    db.session.add(alamat)
    db.session.commit()
    print(f"Data alamat berhasil disimpan: {provinsi_name}, {kabkot_name}, {kecamatan_name}, {kelurahan_name}")

def update_address_in_db(form, alamat, provinsi_choices):
    provinsi_name = dict(provinsi_choices).get(form.provinsi.data, "Provinsi tidak diketahui")
    kabkot_name = dict(get_kabupaten_choices(form.provinsi.data)).get(form.kabkot.data, "Kab/Kota tidak diketahui")
    kecamatan_name = dict(get_kecamatan_choices(form.kabkot.data)).get(form.kecamatan.data, "Kecamatan tidak diketahui")
    kelurahan_name = dict(get_kelurahan_choices(form.kecamatan.data)).get(form.kelurahan.data, "Kelurahan tidak diketahui")
    
    alamat.provinsi = provinsi_name
    alamat.kabkot = kabkot_name
    alamat.kecamatan = kecamatan_name
    alamat.kelurahan = kelurahan_name
    alamat.alamat_lengkap = form.alamatLengkap.data
    alamat.nama_alamat = form.namaAlamat.data
    alamat.provid = form.provinsi.data
    alamat.kabkotid = form.kabkot.data
    alamat.kecid = form.kecamatan.data
    alamat.kelid = form.kelurahan.data
    
    db.session.commit()
    print(f"Data alamat berhasil diperbarui: {provinsi_name}, {kabkot_name}, {kecamatan_name}, {kelurahan_name}")

def cekFormAlamat(form):
    data = {
        'provinsi': get_provinsi_choices(),
        'kabupaten': get_kabupaten_choices(form.provinsi.data) if form.provinsi.data else [],
        'kecamatan': get_kecamatan_choices(form.kabkot.data) if form.kabkot.data else [],
        'kelurahan': get_kelurahan_choices(form.kecamatan.data) if form.kecamatan.data else []
    }
    
    form.provinsi.choices = data['provinsi']
    form.kabkot.choices = data['kabupaten']
    form.kecamatan.choices = data['kecamatan']
    form.kelurahan.choices = data['kelurahan']

    is_valid = bool(form.kecamatan.data)
    return data, is_valid, form
