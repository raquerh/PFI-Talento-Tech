'''
FUNCIONALIDADES:
    ● Registro de productos: La aplicación debe permitir al usuario agregar nuevos productos al inventario, solicitando los siguientes datos: nombre, descripción, cantidad, precio y categoría.
    ● Visualización de productos: La aplicación debe mostrar todos los productos registrados en el inventario, incluyendo su ID, nombre, descripción, cantidad, precio y categoría.
    ● Actualización de productos: La aplicación debe permitir al usuario actualizar la cantidad disponible de un producto específico utilizando su ID.
    ● Eliminación de productos: La aplicación debe permitir al usuario eliminar un producto del inventario utilizando su ID.
    ● Búsqueda de productos: La aplicación debe ofrecer una funcionalidad para buscar productos por su ID, mostrando los resultados que coincidan con los criterios de búsqueda. De manera opcional, se puede implementar la búsqueda por los campos nombre o categoría.
    ● Reporte de Bajo Stock: La aplicación debe generar un reporte de productos que tengan una cantidad igual o inferior a un límite especificado por el usuario.

'''

import sqlite3

def mostrar_menu():
    print("Menú de Gestión de Productos\n")
    print("1. Alta de productos nuevos")
    print("2. Listado completo de productos")
    print("3. Actualizar el stock de un producto")
    print("4. Baja de producto")
    print("5. Consulta de productos")
    print("6. Reporte de productos con bajo stock")
    print("7. Salir\n")

def obtener_opcion():
    while True:
        opcion = int(input("Por favor, selecciona una opción (1-7): "))
        if 1 <= opcion <= 7:
            return opcion
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 7.")

def alta_productos():
    
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("")
    print("Ingreso de nuevos productos")
    print("")

    # Lista para almacenar los productos agregados en esta sesión
    productos_agregados = []
    
    # Usamos el bucle while para ingresar los datos
    while True:
        
        NOMBRE = input("Ingresá el NOMBRE del producto: ").upper()
        DESCRIPCION = input("Ingresá su DESCRIPCION: ").upper()
        CANTIDAD = int(input("Ingresá la CANTIDAD del producto: "))
        PRECIO = float(input("Ingresá su PRECIO unitario: "))
        CATEGORIA = input("Ingresá la CATEGORIA a la que pertenece el producto: ").upper()

    # Verificar si ya existe un producto con la misma DESCRIPCION
        cursor.execute('''
            SELECT COUNT(*) FROM productos WHERE DESCRIPCION = ?;
        ''', (DESCRIPCION,))
        count = cursor.fetchone()[0]

        if count > 0:
            print("Ya existe un producto con la misma DESCRIPCION. No se puede agregar.")
        else:
            cursor.execute('''
                INSERT INTO productos (NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA) VALUES
                (?, ?, ?, ?, ?);
            ''', (NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA))
            conexion.commit()
            print("Producto agregado correctamente.")
            
            # Agregar el producto a la lista de productos agregados
            productos_agregados.append((NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA))
            
        print("")
        salida = input("Desea agregar otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break
            
    # Mostramos  los productos agregados en esta sesion
    print("\nProductos ingresados en esta sesion:\n")
    
    for producto in productos_agregados:
        NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
        print(f"NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}")
        print("")
        
    conexion.close()
    
def listado_completo():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    
    if count > 0:
        # Mostrar productos
        print("Listado completo de productos:\n")
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        for producto in productos:
            id, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f"ID: {id}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}")
            print("")
    else:
        # Mostrar mensaje
        print("No hay productos en el inventario.\n")

    conexion.close()
    
def actualizar_CANTIDAD():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nActualización el stock de productos\n")

    while True:
        # Solicitar al usuario el ID del producto y la nueva CANTIDAD
        id_producto = int(input("Ingresá el ID del producto que deseas actualizar: "))
        
        # Verificar si el ID existe y obtener la CANTIDAD anterior
        cursor.execute('''
            SELECT CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("")
            print("No existe un producto con el ID proporcionado.")
            print("")
        else:
            cantidad_anterior, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA = resultado

            # Imprimir la información del producto antes de solicitar la nueva CANTIDAD
            print("\nProducto seleccionado:")
            print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD_anterior}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            # Solicitar la nueva CANTIDAD
            nueva_cantidad = int(input("Ingresá la nueva cantidad disponible: "))

            # Actualizar la CANTIDAD del producto
            cursor.execute('''
                UPDATE productos SET CANTIDAD = ? WHERE ID = ?;
            ''', (nueva_cantidad, id_producto))
            conexion.commit()

            # Imprimir la información del producto modificado
            print("\nProducto modificado:")
            print("")
            print(f"ID: {id_producto}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}")
            print(f"CANTIDAD ANTERIOR: {cantidad_anterior}, CANTIDAD ACTUAL: {nueva_cantidad}")
            print("")
            
        salida = input("Desea modificar el stock de otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break
    conexion.close()

def eliminar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nEliminar un producto\n")
    productos_eliminados = []

    while True:
        # Solicitar el ID del producto a eliminar
        id_producto = int(input("Ingresá el ID del producto que deseas eliminar: "))
        cursor.execute('''
            SELECT CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("\nNo existe un producto con el ID proporcionado.\n")
        else:
            CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA = resultado
            seguro = input(f"¿Está seguro que desea eliminar el producto:\n ID: {id_producto}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n (s/n) ").upper()
            print("")
            if seguro == "S":
                productos_eliminados.append((id_producto, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA))
                cursor.execute('''
                    DELETE FROM productos WHERE ID = ?;
                ''', (id_producto,))
                conexion.commit()
                print(f"Producto con ID {id_producto} eliminado correctamente.\n")
            else:
                print(f"El producto con ID {id_producto} no fue eliminado.\n")

        salida = input("¿Desea eliminar otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break

    # Mostrar los productos eliminados en esta sesión
    if productos_eliminados:
        print("\nProductos eliminados en esta sesión:\n")
        for producto in productos_eliminados:
            id_producto, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f"ID: {id_producto}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}")
        print("")

    conexion.close()

def consulta_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nConsulta Datos de Productos\n")
    
    while True:
        print("\nOpciones de búsqueda:\n")
        print("1. Por ID")
        print("2. Por NOMBRE")
        print("3. Por DESCRIPCION")
        print("4. Por CANTIDAD")
        print("5. Por PRECIO")
        print("6. Por CATEGORIA")
        print("")
        opcion_busqueda = int(input("Selecciona una opción (1-6): \n"))
        print("")
        print("Has seleccionado la opción de búsqueda número ", opcion_busqueda, "\n")

        match opcion_busqueda:
            case 1:  # Buscar por ID
                id_producto = int(input("Ingrese el codigo del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
                ''', (id_producto,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("\nNo existe un producto con el ID proporcionado.\n")
                else:
                    ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                    print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case 2:  # Buscar por NOMBRE
                Nnombre_producto = input("Ingrese el nombre del producto: ").upper()
                cursor.execute('''
                    SELECT id, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(NOMBRE) LIKE ?;
                ''', (f"%{nombre_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print("\nNo hay productos con el nombre proporcionado.\n")
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case 3:  # Buscar por DESCRIPCION
                DESCRIPCION_producto = input("Ingrese la descripcion del producto: ").upper()
                print("")
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(DESCRIPCION) LIKE ?;
                ''', (f"%{descripcion_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print("\nNo hay productos con esa descripcion.\n")
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case 4:  # Buscar por CANTIDAD
                cantidad_producto = int(input("Ingrese la cantidad del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE CANTIDAD = ?;
                ''', (cantidad_producto,))
                resultados = cursor.fetchall()
                if not resultados:
                    print("\nNo hay productos con esa cantidad.\n")
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case 5:  # Buscar por PRECIO
                precio_producto = float(input("Ingrese el precio del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE PRECIO = ?;
                ''', (precio_producto,))
                resultados = cursor.fetchall()
                if not resultados:
                    print("\nNo hay productos con ese precio.\n")
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case 6:  # Buscar por CATEGORIA
                categoria_producto = input("Ingrese la CATEGORIA del producto: ").upper()
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(CATEGORIA) LIKE ?;
                ''', (f"%{categoria_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print("\nNo hay productos con esa categoria.\n")
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}\n")

            case _:  # Opción no válida
                print("Opción no válida. Por favor, elige una opción entre 1 y 6.")

        seguir = input("¿Desea buscar otro producto? (S/N): ").upper()  # Pregunta si desea seguir buscando  
        if seguir == "N":
            break
    conexion.close()

def reporte_bajo_stock():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nReporte de bajo stock\n")
    productos_bajo_stock = []

    cant_bajo_stock = int(input("Ingrese la cantidad para generar un reporte de los productos que tienen stock menor: "))
    cursor.execute('''
        SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE CANTIDAD <= ?;
    ''', (cant_bajo_stock,))
    resultados = cursor.fetchall()

    for resultado in resultados:
        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
        productos_bajo_stock.append((ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA))

    # Imprimir los productos con bajo stock
    if productos_bajo_stock:
        print("\nProductos con bajo stock:\n")
        for producto in productos_bajo_stock:
            ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f"ID: {ID}, NOMBRE: {NOMBRE}, DESCRIPCION: {DESCRIPCION}, CANTIDAD: {CANTIDAD}, PRECIO: {PRECIO}, CATEGORIA: {CATEGORIA}")
    else:
        print("No hay productos con stock por debajo de la CANTIDAD especificada.")
    conexion.close()
    
while True:

    mostrar_menu()
    opcion = obtener_opcion()

    match opcion:
        case 1:
            alta_productos()
        case 2:
            listado_completo()
        case 3:
            actualizar_CANTIDAD()
        case 4:
            eliminar_producto()
        case 5:
            consulta_producto()
        case 6:
            reporte_bajo_stock()
        case 7:
            print("Saliendo del programa.")
            break
        case _:
            print("Opción no válida. Por favor, elige una opción entre 1 y 7.")
