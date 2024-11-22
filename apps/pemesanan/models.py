from sqlalchemy import func
from apps import db


class Bengkel(db.Model):
    _tablename_ = 'bengkel'
    bengkelId = db.Column(db.Integer, primary_key=True)
    namaBengkel = db.Column(db.String(30), nullable=False)
    lokasi = db.Column(db.String(50), nullable=False)
    noTelp = db.Column(db.Integer, nullable=False)

    montirs = db.relationship('Montir', backref='bengkel', lazy=True)
    products = db.relationship('Product', backref='bengkel', lazy=True)

class Montir(db.Model):
    _tablename_ = 'montir'
    montirId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(10), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.Boolean, nullable=False)
    tanggalLahir = db.Column(db.Date, nullable=False)
    tempatLahir = db.Column(db.String(15), nullable=False)
    bengkelIdFK = db.Column(db.Integer, db.ForeignKey('bengkel.bengkelId'), nullable=False)
    is_availaible = db.Column(db.Boolean, nullable = True)

    orders = db.relationship('Orders', backref='montir', lazy=True)

class Orders(db.Model):
    _tablename_ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=True)
    lokasi = db.Column(db.String(50), nullable=False)
    userIdFK = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    montirIdFK = db.Column(db.Integer, db.ForeignKey('montir.montirId'), nullable=False)

    product_details = db.relationship('ProductDetails', backref='order', lazy=True)

class Product(db.Model):
    _tablename_ = 'product'
    productId = db.Column(db.Integer, primary_key=True)
    namaProduct = db.Column(db.String(30), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    hargaPerSatuan = db.Column(db.Integer, nullable=False)
    bengkelIdFK = db.Column(db.Integer, db.ForeignKey('bengkel.bengkelId'), nullable=False)
    categoryIdFK = db.Column(db.Integer, db.ForeignKey('category.categoryId'), nullable=False)

class Category(db.Model):
    _tablename_ = 'category'
    categoryId = db.Column(db.Integer, primary_key=True)
    namaCategory = db.Column(db.String(20), nullable=False)
    deskripsi = db.Column(db.String(150), nullable=True)

    products = db.relationship('Product', backref='category', lazy=True)

class ProductDetails(db.Model):
    _tablename_ = 'productdetails'
    productDetailsId = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True)
    productIdFK = db.Column(db.Integer, db.ForeignKey('product.productId'), nullable=True)
    ordersIdFK = db.Column(db.Integer, db.ForeignKey('orders.orderID'), nullable=False)