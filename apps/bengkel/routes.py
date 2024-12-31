from flask import render_template, redirect, request, url_for,jsonify
from flask_login import (
    current_user,
    login_required
)
from flask import flash
from apps import db
from apps.bengkel import blueprint
from apps.authentication.Montir import Montir
from apps.authentication.Bengkel import Bengkel
from apps.bengkel.Pending import Pending
from apps.bengkel.forms import TambahMontirForm, KategoriForm, ProductForm
from apps.pemesanan.models import Category, Product, Orders
def format_to_idr(value):
    return f"Rp {value:,.0f}".replace(",", ".")

@blueprint.route('/dashboard')
@login_required(role="Bengkel")
def dashboard():
    bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
    return render_template('bengkel/dashboard.html',bengkel=bengkel)

@blueprint.route('/montir')
@login_required(role="Bengkel")
def montir_page():
    bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
    montirs = Montir.query.filter_by(bengkelIdFK=bengkel.bengkelId)
    montir_data = [
        {
            'montir':montir,
            'gajiIDR':format_to_idr(montir.gaji)
        }
        for montir in montirs
    ]
    return render_template('bengkel/montir_page.html', montirs = montir_data, segment = 'montir',bengkel=bengkel)

@blueprint.route('/tambah-montir', methods = ['GET', 'POST']) 
@login_required(role="Bengkel")
def tambah_montir():
    form = TambahMontirForm()

    
    bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
    if form.validate_on_submit():
        montir = Montir.query.filter_by(montirId=form.idMontir.data).first()
        
        if montir and not montir.bengkelIdFK:
            pending = Pending(
                montir_id_fk = montir.montirId,
                bengkel_id_fk = bengkel.bengkelId,
                gaji = form.gaji.data,
                jabatan = form.jabatan.data,
                deadline = form.deadline.data
            )
            db.session.add(pending)
            db.session.commit()
            flash('Montir berhasil ditambahkan ke dalam daftar pending.', 'success')
            return redirect(url_for('bengkel_blueprint.montir_page'))
        else:
            flash('Montir tidak tersedia untuk direkrut.', 'danger')
            return render_template('bengkel/tambah_montir.html', form = form,bengkel=bengkel)

        
    
    return render_template('bengkel/tambah_montir.html', form = form,bengkel=bengkel)

# @blueprint.route('/tambah-kategori', methods=['POST'])
# def tambah_kategori():
#     form = KategoriForm()
#     bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
#     if form.validate_on_submit():
#         new_category = Category(
#             namaCategory=form.namaCategory.data,
#             deskripsi=form.deskripsi.data,
#             bengkel_id_fk= bengkel.bengkelId
#         )
#         db.session.add(new_category)
#         db.session.commit()
#         flash('Kategori berhasil ditambahkan!', 'success')
#         return redirect(url_for('bengkel_blueprint.daftar_produk'))
    

# @blueprint.route('/produk', methods = ['GET', 'POST']) 
# @login_required(role="Bengkel")
# def daftar_produk():
#     bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
    
#     # Menginisialisasi form dengan ID bengkel yang sedang login
#     form = ProductForm(bengkel_id=bengkel.bengkelId)

#     if form.validate_on_submit():
#         # Mengambil data dari form
#         nama_product = form.namaProduct.data
#         harga_per_satuan = form.hargaPerSatuan.data
#         stock = form.stock.data
#         category_id = form.category.data
        
#         # Membuat produk baru
#         new_product = Product(
#             namaProduct=nama_product,
#             hargaPerSatuan=harga_per_satuan,
#             stock=stock,
#             categoryIdFK=category_id,
#             bengkelIdFK=bengkel.bengkelId  # Menggunakan bengkel yang sedang login
#         )
        
#         db.session.add(new_product)
#         db.session.commit()
#         return redirect(url_for('bengkel_blueprint.daftar_produk'))
    
#     # Mengambil produk yang terkait dengan bengkel yang login
#     products = Product.query.filter_by(bengkelIdFK=bengkel.bengkelId).all()
#     return render_template('bengkel/produk.html',
#                            segment="produk", 
#                            bengkel=bengkel,
#                            form=form, products=products)
@blueprint.route('/produk', methods=['GET', 'POST'])
@login_required(role="Bengkel")
def daftar_produk():
    bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()

    # Form Produk
    product_form = ProductForm(bengkel_id=bengkel.bengkelId)

    # Form Kategori
    category_form = KategoriForm()

    # Proses Form Produk
    if product_form.validate_on_submit() and 'submit_product' in request.form:
        new_product = Product(
            namaProduct=product_form.namaProduct.data,
            hargaPerSatuan=product_form.hargaPerSatuan.data,
            stock=product_form.stock.data,
            categoryIdFK=product_form.category.data,
            bengkelIdFK=bengkel.bengkelId
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Produk berhasil ditambahkan!', 'success')
        return redirect(url_for('bengkel_blueprint.daftar_produk'))

    # Proses Form Kategori
    if category_form.validate_on_submit() and 'submit_category' in request.form:
        new_category = Category(
            namaCategory=category_form.namaCategory.data,
            deskripsi=category_form.deskripsi.data,
            bengkel_id_fk=bengkel.bengkelId
        )
        db.session.add(new_category)
        db.session.commit()
        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('bengkel_blueprint.daftar_produk'))

    # Ambil data untuk ditampilkan
    products = Product.query.filter_by(bengkelIdFK=bengkel.bengkelId).all()

    return render_template(
        'bengkel/produk.html',
        segment="produk",
        bengkel=bengkel,
        product_form=product_form,
        category_form=category_form,
        products=products
    )

@blueprint.route('/update-product', methods=['POST'])
@login_required(role="Bengkel")
def update_product():
    data = request.get_json()
    product_id = data.get('id')
    nama_product = data.get('namaProduct')
    harga_per_satuan = data.get('hargaPerSatuan')
    stock = data.get('stock')
    category_id = data.get('categoryId')

    print(f"Product ID: {product_id}")

    product = Product.query.get(product_id)
    if product:
        product.namaProduct = nama_product
        product.hargaPerSatuan = harga_per_satuan
        product.stock = stock
        product.categoryIdFK = category_id
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Produk tidak ditemukan!"}), 404

@blueprint.route('/delete-product', methods=['DELETE'])
@login_required(role="Bengkel")
def delete_product():
    data = request.get_json()
    product_id = data.get('id')
    print("DIKLIK")
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Produk tidak ditemukan!"}), 404

@blueprint.route('/transaksi',methods = ['GET'])
@login_required(role="Bengkel")
def transaksi():
    bengkel = Bengkel.query.filter_by(user_id_fk=current_user.id).first()
    orders = Orders.query.filter_by(bengkel_id_fk=bengkel.bengkelId).all()
    return render_template('bengkel/daftar_transaksi.html',
                           segment = "transaksi",
                           orders = orders,
                           bengkel=bengkel)

