from sqlalchemy import func
from apps import db


class Orders(db.Model):
    _tablename_ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=True)
    lokasi = db.Column(db.String(50), nullable=False)
    userIdFK = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    montirIdFK = db.Column(db.Integer, db.ForeignKey('montir.montirId'), nullable=False)
    bengkel_id_fk = db.Column(db.Integer, db.ForeignKey('bengkel.bengkelId'))
    customer_id_fk = db.Column(db.Integer, db.ForeignKey('customer.id'))
    kendaraan_id_fk = db.Column(db.Integer, db.ForeignKey('vehicles.vehicleID'))
    keluhan = db.Column(db.String(50))
    status = db.Column(db.String(50))
    task_id = db.Column(db.String(50))

    orderDetails = db.relationship('OrderDetails',backref='orders-orderDetail',lazy=True)
    user = db.relationship('Users',backref='order-user',lazy=True)
    customer = db.relationship('Customer',backref = 'customer', lazy=True)
    montir = db.relationship('Montir',backref = 'orders', lazy=True)
    bengkel = db.relationship('Bengkel',backref = 'orders', lazy =True)
    vehicle = db.relationship('Vehicles',backref = 'orders-vehicle', lazy =True)

class Product(db.Model):
    _tablename_ = 'product'
    productId = db.Column(db.Integer, primary_key=True,nullable=False)
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
    bengkel_id_fk = db.Column(db.Integer, db.ForeignKey('bengkel.bengkelId'), nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

class OrderDetails(db.Model):
    _tablename_ = 'orderDetails'
    id = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(10))
    order_id_fk = db.Column(db.Integer, db.ForeignKey('orders.orderID'))
    produk_id_fk = db.Column(db.Integer, db.ForeignKey('product.productId'))
    deskripsi = db.Column(db.String(150))
    hargaJenis = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    
    produk = db.relationship('Product', backref = 'OrderDetails-Product', lazy = True)