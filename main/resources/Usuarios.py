from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel


class Usuario(Resource):
    def get(self,id): #obtener 1 en especifico
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try:
            return usuario.to_json()
        except:    
            return 'Resource not found', 404

    def put(self,id): #editar
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        try:#el ORM comprueba que existe el producto y lo actualiza
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        except:
            return ' ', 404

    def delete(self,id): #eliminar
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
        except:
            return ' ', 404


class Usuarios(Resource):
    def get(self): #obtener todos
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify({
            'Compras': [usuario.to_json() for usuario in usuarios]
        })
    
    # def post(self): #agregar varios
    #     usuario = UsuarioModel.from_json(request.get_json())
    #     db.session.add(usuario)
    #     db.session.commit()
    #     return usuario.to_json(), 201