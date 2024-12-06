'''
1- Crear una base de datos SQLite llamada 'inventario.db' para almacenar los datos de los productos.
2- La tabla 'productos' debe contener las siguientes columnas:
    ● 'id': Identificador único del producto (clave primaria, autoincremental).
    ● 'nombre': Nombre del producto (texto, no nulo).
    ● 'descripcion': Breve descripción del producto (texto).
    ● 'cantidad': Cantidad disponible del producto (entero, no nulo).
    ● 'precio': Precio del producto (real, no nulo).
    ● 'categoria': Categoría a la que pertenece el producto (texto).
'''

import sqlite3
def crear_tabla_productos():
# Conectar a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    # eliminar la tabla si existe
    # cursor.execute('''
    #     DROP TABLE IF EXISTS productos;
    #     ''')
    # Crear la tabla Productos si no existe
    cursor.execute('''
        CREATE TABLE productos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT    NOT NULL,
            descripcion TEXT  NOT NULL,
            cantidad  INTEGER NOT NULL,
            precio    REAL    NOT NULL,
            categoria TEXT    NOT NULL
        )
        STRICT;
    ''')
    # Confirmar la creación de la tabla y cerrar la conexión
    conexion.commit()
    conexion.close()
    print("Tabla Productos creada con éxito.")
    # Llamar a la función para crear la tabla

crear_tabla_productos()