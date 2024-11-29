from apps import db

class Alamat(db.Model):
    __tablename__ = 'alamat'
    alamatID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)

    user = db.relationship('Users', backref='user_addresses', foreign_keys=[userID])