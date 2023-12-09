#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask import request
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app) # Esto habilitará CORS para todas las rutas


class Catalogo:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err


        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS formulario_datos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            empresa VARCHAR(255) NOT NULL,
            correo VARCHAR(255) NOT NULL,
            cantidad_empleados INT NOT NULL,
            servicio VARCHAR(255) NOT NULL
            )
          ''')  
        self.conn.commit()


        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)


    #----------------------------------------------------------------
    def listar_cotizaciones(self):
        self.cursor.execute("SELECT * FROM formulario_datos")
        cotizaciones = self.cursor.fetchall()
        return cotizaciones

    #----------------------------------------------------------------
    def consultar_cotizacion(self, id):
        self.cursor.execute("SELECT * FROM formulario_datos WHERE id = %s", (id,))
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def agregar_formulario_datos(self, nombre, empresa, correo, cantidad_empleados, servicio):
      # Asegúrate de que la indentación de este bloque esté alineada con la del resto de tu código
      sql = "INSERT INTO formulario_datos (nombre, empresa, correo, cantidad_empleados, servicio) VALUES (%s, %s, %s, %s, %s)"
      valores = (nombre, empresa, correo, cantidad_empleados, servicio)
      self.cursor.execute(sql, valores)
      self.conn.commit()
      return True


    #----------------------------------------------------------------
    def eliminar_cotizacion(self, id):
      # Eliminamos una cotización de la tabla a partir de su identificador
      self.cursor.execute("DELETE FROM formulario_datos WHERE id = %s", (id,))
      self.conn.commit()
      return self.cursor.rowcount > 0


    #----------------------------------------------------------------
    def modificar_cotizacion(self, id, nuevo_nombre, nueva_empresa, nuevo_correo, nueva_cantidad_empleados, nuevo_servicio):
      sql = "UPDATE formulario_datos SET nombre = %s, empresa = %s, correo = %s, cantidad_empleados = %s, servicio = %s WHERE id = %s"
      valores = (nuevo_nombre, nueva_empresa, nuevo_correo, nueva_cantidad_empleados, nuevo_servicio, id)
      self.cursor.execute(sql, valores)
      self.conn.commit()
      return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    @app.route("/cotizaciones/<int:id>", methods=["GET"])
    def obtener_cotizacion(id):
      # Lógica para obtener una cotización específica
      cotizacion = catalogo.consultar_cotizacion(id)
      if cotizacion:
          return jsonify(cotizacion)
      else:
          return "Cotización no encontrada", 404


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='sergio', password='vbOkOnly1@', database='miapp')
cotizaciones = catalogo.listar_cotizaciones()  # Llamando al método listar_cotizaciones


# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'


#--------------------------------------------------------------------
@app.route("/cotizaciones", methods=["GET"])
def listar_cotizaciones():
    cotizaciones = catalogo.listar_cotizaciones()
    print(cotizaciones)
    return jsonify(cotizaciones)



#--------------------------------------------------------------------
@app.route("/cotizaciones/<int:id>", methods=["GET"])
def mostrar_cotizacion(id):
    cotizacion = catalogo.consultar_cotizacion(id)
    if cotizacion:
        return jsonify(cotizacion)
    else:
        return "Cotización no encontrada", 404


@app.route("/formulario_datos", methods=["POST"])
def agregar_datos_formulario():
    # Recojo los datos del form
    nombre = request.form['nombre']
    empresa = request.form['empresa']
    correo = request.form['correo']
    cantidad_empleados = request.form['cantidadEmpleados']
    servicio = request.form['servicio']

    if catalogo.agregar_formulario_datos(nombre, empresa, correo, cantidad_empleados, servicio):
        return jsonify({"mensaje": "Datos del formulario agregados"}), 201
    else:
        return jsonify({"mensaje": "Error al agregar los datos"}), 400


@app.route("/cotizaciones/<int:id>", methods=["DELETE"])
def eliminar_cotizacion(id):
    # Verifica si la cotización existe
    cotizacion = catalogo.consultar_cotizacion(id)
    if cotizacion:
        # Elimina la cotización del catálogo
        if catalogo.eliminar_cotizacion(id):
            return jsonify({"mensaje": "Cotización eliminada"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar la cotización"}), 500
    else:
        return jsonify({"mensaje": "Cotización no encontrada"}), 404

@app.route("/cotizaciones/<int:id>", methods=["PUT"])
def modificar_cotizacion(id):
    # Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nueva_empresa = request.form.get("empresa")
    nuevo_correo = request.form.get("correo")
    nueva_cantidad_empleados = request.form.get("cantidadEmpleados")
    nuevo_servicio = request.form.get("servicio")

    # Actualización de la cotización
    if catalogo.modificar_cotizacion(id, nuevo_nombre, nueva_empresa, nuevo_correo, nueva_cantidad_empleados, nuevo_servicio):
        return jsonify({"mensaje": "Cotización modificada"}), 200
    else:
        return jsonify({"mensaje": "Cotización no encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
