import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

DB_HOST = 'localhost'
DB_USER = 'Brian'
DB_PASSWORD = 'k3S5bhÑqre87het86veR'
DB_NAME = 'miapp'
DB_PORT = '3306'

class Catalogo:
    def __init__(self, host, user, password, database, port):
        self.conexion = mysql.connector.connect(  
        #conecta con BD
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.crear_tabla()
        #controla que exista tabla cuando se crea instancia

    def crear_tabla(self):
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                codigo INT AUTO_INCREMENT PRIMARY KEY,
                descripcion VARCHAR(255) NOT NULL,
                cantidad INT(4) NOT NULL,
                precio DECIMAL(10, 2) NOT NULL,
                imagen_url VARCHAR(255),
                proveedor INT(3)
            )''')
        except Error as e:
            print(f'Error al crear la tabla: {e}')
        finally:
            cursor.close()
        self.conexion.commit()

    def conectar(self):
        return self.conexion

    def desconectar(self):
        self.conexion.close()

    def ejecutar_consulta(self, consulta, parametros=None):
    #consulta: 'SELECT','INSERT',etc. / parametros: tupla de parámetros 
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(consulta, parametros)
            #ejecuta la consulta
            if consulta.strip().upper().startswith('SELECT'):
            #controla si consulta es 'SELECT' o no
                resultado = cursor.fetchall()
                #guarda resultado de consulta
            else:
                self.conexion.commit()
                resultado = cursor.rowcount
                #guarda numero de filas afectadas
            return resultado
        except Error as e:
        #controla posibles errores
            print(f'Error al ejecutar la consulta: {e}')
            return None
        finally:
            cursor.close()
            #cierra cursor sí o sí

    def consultar_producto(self, codigo):
        consulta = 'SELECT * FROM productos WHERE codigo = %s'
        resultado = self.ejecutar_consulta(consulta, (codigo,)) 
        return resultado[0] if resultado else None

    def agregar_producto(self, descripcion, cantidad, precio, imagen, proveedor):
        consulta = 'INSERT INTO productos (descripcion, cantidad, precio, imagen_url, proveedor) VALUES (%s, %s, %s, %s, %s)'
        return self.ejecutar_consulta(consulta, (descripcion, cantidad, precio, imagen, proveedor))

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor):
        consulta = 'UPDATE productos SET descripcion=%s, cantidad=%s, precio=%s, imagen_url=%s, proveedor=%s WHERE codigo=%s'
        return self.ejecutar_consulta(consulta, (nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_imagen, nuevo_proveedor, codigo))

    def eliminar_producto(self, codigo):
        consulta = 'DELETE FROM productos WHERE codigo=%s'
        return self.ejecutar_consulta(consulta, (codigo,))

@app.route('/')
def index():
    return render_template('index.html')
    #renderiza el 'index.html'

@app.route('/productos', methods=['POST'])
def crear_producto():
    catalogo = Catalogo(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    nuevo_producto = request.json
    catalogo.agregar_producto(nuevo_producto['descripcion'], nuevo_producto['cantidad'], nuevo_producto['precio'], nuevo_producto['imagen'], nuevo_producto['proveedor'])
    catalogo.desconectar()
    return jsonify({'mensaje':'Producto agregado exitosamente'}), 201

@app.route('/productos/<int:codigo>', methods=['GET'])
def encontrar_producto(codigo):
    catalogo = Catalogo(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    producto = catalogo.consultar_producto(codigo)
    catalogo.desconectar()
    if producto:
        return jsonify(producto), 200
    else:
        return jsonify({'mensaje': 'Producto no encontrado'}), 404

@app.route('/productos/<int:codigo>', methods=['PUT'])
def actualizar_producto(codigo):
    catalogo = Catalogo(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    datos = request.json
    catalogo.modificar_producto(codigo, datos['descripcion'], datos['cantidad'], datos['precio'], datos['imagen'], datos['proveedor'])
    catalogo.desconectar()
    return jsonify({'mensaje': 'Producto actualizado exitosamente'}), 200

@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    catalogo = Catalogo(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    catalogo.eliminar_producto(codigo)
    catalogo.desconectar()
    return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200

if __name__ == '__main__':
    app.run(debug=True)
