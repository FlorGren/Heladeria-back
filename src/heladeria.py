from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from config import config

app = Flask(__name__)

CORS(app)

conexion = MySQL(app)

# -----------------------------------------------------------------

@app.route('/sabor', methods=['GET'])
def listar_sabores():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, imagen FROM sabores"
        cursor.execute(sql)
        productos = cursor.fetchall()
        sabor = []
        for fila in productos:
            sabores = {'codigo': fila[0], 'nombre': fila[1], 'imagen': fila[2]}
            sabor.append(sabores)
        return jsonify(sabor)
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# -----------------------------------------------------------------

def mostrar_sabores_bd(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM sabores WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        productos = cursor.fetchone()
        if productos != None:
                sabores = {'codigo': productos[0], 'nombre': productos[1], 'imagen': productos[2]}
                return sabores
        else:
            return None
    except Exception as ex:
        print ("ex", ex)

# -----------------------------------------------------------------

@app.route('/sabor/<codigo>', methods=['GET'])
def mostrar_sabores(codigo):
        try:
            sabores = mostrar_sabores_bd(codigo)
            if sabores != None:
                return jsonify({'sabores': sabores, 'mensaje': "Sabor encontrado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Sabor no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

# -----------------------------------------------------------------

@app.route('/sabor', methods=['POST'])
def agregar_sabores():
        try:
            sabores = mostrar_sabores_bd(request.json['codigo']) 
            if sabores != None:
                return jsonify({'mensaje': "Código ya existente, no se puede duplicar.", 'exito': False})
            else:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO sabores (codigo, nombre, imagen) VALUES ({0}, '{1}', '{2}')""".format(request.json['codigo'],
                                                                                                           request.json['nombre'], request.json['imagen'])
                cursor.execute(sql)
                conexion.connection.commit()
            return jsonify({'mensaje': "Sabor registrado.", 'exito': True})
        except Exception:
            return jsonify({'mensaje': "Error", 'exito': False})

# ----------------------------------------------------------------

@app.route('/sabor/<codigo>', methods=['PUT'])
def modificar_sabores(codigo):
    try:
        sabores = mostrar_sabores_bd(codigo)
        if sabores != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE sabores SET nombre = '{0}', imagen = '{1}'
            WHERE codigo = {2}""".format(request.json['nombre'], request.json['imagen'], codigo)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Sabor actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Sabor no encontrado.", 'exito': False})
    except Exception:
            return jsonify({'mensaje': "Error", 'exito': False})

# ----------------------------------------------------------------

@app.route('/sabor/<codigo>', methods=['DELETE'])
def eliminar_sabores(codigo):
    try:
        sabores = mostrar_sabores_bd(codigo)
        if sabores != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM sabores WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Sabor eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Sabor no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# ----------------------------------------------------------------

if __name__ == '__main__':
    app.config.from_object(config['development'])
    #app.register_error_handler(404, pagina_no_encontrada)
    app.run()