from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompra(Resource):
    def get(self,id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            return productocompra.to_json()
        except:    
            return 'Resource not found', 404

    def put(self,id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(productocompra, key, value)
        try:#el ORM comprueba que existe el producto y lo actualiza
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json(), 201
        except:
            return ' ', 404

    def delete(self,id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
            return ' ', 204
        except:
            return ' ', 404

class ProductosCompras(Resource):
    def get(self):
        productoscompras = db.session.query(ProductoCompraModel).all()
        return jsonify({
            'productoscompras': [productocompra.to_json() for productocompra in productoscompras]
        })
    
    def post(self):
        productocompra = ProductoCompraModel.from_json(request.get_json())
        db.session.add(productocompra)
        db.session.commit()
        return productocompra.to_json(), 201