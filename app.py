from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión con la base de datos
def conectar():
    conexion = sqlite3.connect("tienda.db")
    conexion.row_factory = sqlite3.Row
    return conexion


# Crear tabla de productos
def crear_tabla():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# Página principal: registrar productos
@app.route("/")
def inicio():
    return render_template("index.html")


# Guardar productos
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = float(request.form["precio"])
    cantidad = int(request.form["cantidad"])
    categoria = request.form["categoria"]

    conexion = conectar()

    conexion.execute("""
        INSERT INTO productos
        (nombre, descripcion, precio, cantidad, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, precio, cantidad, categoria))

    conexion.commit()
    conexion.close()

    return redirect(url_for("mostrar_productos"))


# Consultar todos los productos
@app.route("/productos")
def mostrar_productos():
    conexion = conectar()

    productos = conexion.execute(
        "SELECT * FROM productos ORDER BY id DESC"
    ).fetchall()

    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# Ejecutar aplicación
if __name__ == "__main__":
    crear_tabla()
    app.run(debug=True)