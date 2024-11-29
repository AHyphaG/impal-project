from flask import Blueprint

blueprint = Blueprint(
    'pemesanan_blueprint',
    __name__,
    url_prefix='/pemesanan'
)