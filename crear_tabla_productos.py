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
            ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE   TEXT    NOT NULL,
            DESCRIPCION TEXT  NOT NULL,
            CANTIDAD  INTEGER NOT NULL,
            PRECIO   REAL    NOT NULL,
            CATEGORIA TEXT    NOT NULL
        )
        STRICT;
    ''')
        
    cursor.execute('''
        INSERT INTO productos (NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA) VALUES
        ('CASCO INTEGRAL', 'CASCO PROTECTOR INTEGRAL CON CERTIFICACION DOT', 20, 120.00, 'ACCESORIOS'),
        ('GUANTES DE MOTO', 'GUANTES DE CUERO CON PROTECCIONES PARA LOS NUDILLOS', 35, 45.99, 'ROPA'),
        ('LUZ LED PARA FAROS', 'KIT DE LUCES LED DE ALTA INTENSIDAD PARA FAROS DELANTEROS', 50, 35.50, 'ILUMINACION'),
        ('BATERIA PARA MOTO', 'BATERIA DE GEL DE 12V, COMPATIBLE CON LA MAYORIA DE MODELOS', 15, 80.00, 'REPUESTOS'),
        ('ACEITE PARA MOTOR', 'BOTELLA DE 1L DE ACEITE SINTETICO PARA MOTOS 4 TIEMPOS', 60, 15.99, 'MANTENIMIENTO'),
        ('CHAQUETA DE MOTO', 'CHAQUETA CON PROTECCIONES RESISTENTES AL AGUA Y AL VIENTO', 10, 150.00, 'ROPA'),
        ('CAMARA DE AIRE', 'CAMARA DE AIRE DE 18 PULGADAS PARA NEUMATICOS TRASEROS', 40, 12.50, 'REPUESTOS'),
        ('FILTRO DE AIRE', 'FILTRO DE AIRE DE ALTO FLUJO COMPATIBLE CON MOTOS DEPORTIVAS', 25, 25.99, 'MANTENIMIENTO'),
        ('CANDADO DE DISCO', 'CANDADO DE SEGURIDAD ANTIRROBO CON ALARMA', 30, 22.75, 'SEGURIDAD'),
        ('SOPORTE PARA CELULAR', 'SOPORTE AJUSTABLE PARA CELULAR RESISTENTE A VIBRACIONES', 50, 18.99, 'ACCESORIOS'),
        ('KIT DE HERRAMIENTAS', 'KIT COMPACTO CON LLAVES Y DESTORNILLADORES ESPECIFICOS PARA MOTOS', 15, 40.00, 'HERRAMIENTAS'),
        ('CHALECO REFLECTANTE', 'CHALECO CON FRANJAS REFLECTANTES PARA MAYOR VISIBILIDAD', 60, 10.99, 'SEGURIDAD'),
        ('PASTILLAS DE FRENO', 'SET DE PASTILLAS DE FRENO DELANTERAS Y TRASERAS', 30, 25.50, 'REPUESTOS'),
        ('LLANTA PARA MOTO', 'LLANTA PARA TERRENOS MIXTOS, TAMAÑO 130/70-17', 20, 75.00, 'REPUESTOS'),
        ('CARGADOR USB PARA MOTO', 'CARGADOR RESISTENTE AL AGUA CON DOBLE PUERTO USB', 40, 15.00, 'ACCESORIOS'),
        ('KIT DE LUCES AUXILIARES', 'LUCES LED AUXILIARES PARA MEJORAR LA VISIBILIDAD EN CARRETERA', 25, 50.00, 'ILUMINACION'),
        ('PROTECTOR DE TANQUE', 'ADHESIVO PROTECTOR DE TANQUE DE COMBUSTIBLE ANTIDESLIZANTE', 40, 12.00, 'ACCESORIOS'),
        ('ESCAPE DEPORTIVO', 'SISTEMA DE ESCAPE DE ALTO RENDIMIENTO PARA MOTOS DEPORTIVAS', 8, 200.00, 'REPUESTOS'),
        ('ESPEJOS RETROVISORES', 'JUEGO DE ESPEJOS RETROVISORES AJUSTABLES UNIVERSALES', 30, 25.00, 'REPUESTOS'),
        ('MALETA TRASERA', 'MALETA RIGIDA IMPERMEABLE CON CAPACIDAD DE 30 LITROS', 12, 85.00, 'ACCESORIOS'),
        ('KIT DE CADENAS', 'CADENA REFORZADA CON PIÑON Y PLATO PARA MOTOS DE ALTO CILINDRAJE', 10, 60.00, 'REPUESTOS'),
        ('CUBIERTA PARA MOTO', 'FUNDA IMPERMEABLE Y RESISTENTE AL POLVO PARA PROTEGER LA MOTO', 50, 30.00, 'ACCESORIOS'),
        ('PAR DE INTERMITENTES LED', 'INTERMITENTES LED UNIVERSALES CON DISEÑO COMPACTO', 40, 20.00, 'ILUMINACION'),
        ('BOLSA PARA TANQUE', 'BOLSA MAGNETICA PARA TANQUE CON COMPARTIMENTO PARA MAPA O CELULAR', 20, 40.00, 'ACCESORIOS'),
        ('BOTAS DE MOTO', 'BOTAS DE CUERO CON PROTECCION PARA TOBILLOS Y SUELA ANTIDESLIZANTE', 15, 120.00, 'ROPA'),
        ('GUARDABARROS TRASERO', 'GUARDABARROS DE PLASTICO RESISTENTE PARA MOTOS DE CROSS', 25, 45.00, 'REPUESTOS'),
        ('SET DE CALCOS', 'CALCOS REFLECTANTES DE ALTA CALIDAD PARA PERSONALIZACION', 60, 10.50, 'ACCESORIOS'),
        ('CUBREPUÑOS CALEFACTABLES', 'CUBREPUÑOS CON SISTEMA DE CALEFACCION PARA CLIMAS FRIOS', 10, 55.00, 'ACCESORIOS'),
        ('CASCOS ABIERTOS', 'CASCO ABIERTO CON VISERA, IDEAL PARA CIUDAD', 18, 75.00, 'ACCESORIOS'),
        ('PROTECTOR DE RODILLAS', 'PROTECCIONES AJUSTABLES PARA RODILLAS Y ESPINILLAS', 30, 30.00, 'ROPA'),
        ('CAMARA PARA CASCO', 'CAMARA DE ACCION HD PARA GRABAR TUS RECORRIDOS', 10, 95.00, 'ACCESORIOS'),
        ('PINTURA EN SPRAY', 'PINTURA ESPECIAL PARA RESTAURAR EL COLOR DE CARENADOS', 40, 12.00, 'MANTENIMIENTO'),
        ('MANILLARES DEPORTIVOS', 'MANILLARES DE ALUMINIO AJUSTABLES PARA MAYOR CONFORT', 20, 40.00, 'REPUESTOS'),
        ('CASCO MODULAR', 'CASCO MODULAR CON DOBLE VISERA Y SISTEMA DE VENTILACION', 15, 135.00, 'ACCESORIOS'),
        ('ACEITE PARA CADENA', 'LUBRICANTE EN SPRAY PARA CADENAS DE TRANSMISION', 50, 10.99, 'MANTENIMIENTO');

    ''')

    # Confirmar la creación de la tabla y cerrar la conexión
    conexion.commit()
    conexion.close()
    print("Tabla Productos creada con éxito.")
    # Llamar a la función para crear la tabla

crear_tabla_productos()