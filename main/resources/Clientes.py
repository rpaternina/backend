from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel



class Cliente(Resource):

    def get(self, id): #obtener 1 en especifico
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        try:
            return cliente.to_json()
        except:    
            return 'Resource not found', 404

    def put(self,id): #editar
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(cliente, key, value)
        try: #El ORM comprueba que existe el producto y lo actualiza
            db.session.add(cliente)
            db.session.commit()
            return cliente.to_json(), 201
        except:
            return ' ', 404

    def delete(self,id): #eliminar
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(cliente)
            db.session.commit()
            return ' ', 204
        except:
            return ' ', 404


class Clientes(Resource):
    
    def get(self): #obtener todos
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente').a
        return jsonify({
            'Compras': [cliente.to_json() for cliente in clientes]
        })
    
    def post(self): #agregar varios
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.role = 'cliente'
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201