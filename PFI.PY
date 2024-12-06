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
    print("3. Actualizar cantidad de un producto")
    print("4. Baja de producto")
    print("5. Consulta de productos")
    print("6. Lista de productos con bajo stock")
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
        
        nombre = input("Ingresá el nombre del producto: ").upper()
        descripcion = input("Ingresá su descripción: ").upper()
        cantidad = int(input("Ingresá la cantidad del producto: "))
        precio = float(input("Ingresá su precio unitario: "))
        categoria = input("Ingresá la categoria a la que pertenece el producto: ").upper()

    # Verificar si ya existe un producto con la misma descripción
        cursor.execute('''
            SELECT COUNT(*) FROM productos WHERE descripcion = ?;
        ''', (descripcion,))
        count = cursor.fetchone()[0]

        if count > 0:
            print("Ya existe un producto con la misma descripción. No se puede agregar.")
        else:
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES
                (?, ?, ?, ?, ?);
            ''', (nombre, descripcion, cantidad, precio, categoria))
            conexion.commit()
            print("Producto agregado correctamente.")
            
            # Agregar el producto a la lista de productos agregados
            productos_agregados.append((nombre, descripcion, cantidad, precio, categoria))
            
        print("")
        salida = input("Desea agregar otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break
            
    # Mostramos  los productos agregados en esta sesion
    print("\nProductos ingresados en esta sesion:\n")
    
    for producto in productos_agregados:
        nombre, descripcion, cantidad, precio, categoria = producto
        print(f"Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}")
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
            id, nombre, descripcion, cantidad, precio, categoria = producto
            print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}")
            print("")
    else:
        # Mostrar mensaje
        print("No hay productos en el inventario.\n")

    conexion.close()
    
def actualizar_cantidad():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nActualización de cantidad de productos\n")

    while True:
        # Solicitar al usuario el ID del producto y la nueva cantidad
        id_producto = int(input("Ingresá el ID del producto que deseas actualizar: "))
        nueva_cantidad = int(input("Ingresá la nueva cantidad disponible: "))

        # Verificar si el ID existe y obtener la cantidad anterior
        cursor.execute('''
            SELECT cantidad, nombre, descripcion, precio, categoria FROM productos WHERE id = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("")
            print("No existe un producto con el ID proporcionado.")
            print("")
        else:
            cantidad_anterior, nombre, descripcion, precio, categoria = resultado

            # Actualizar la cantidad del producto
            cursor.execute('''
                UPDATE productos SET cantidad = ? WHERE id = ?;
            ''', (nueva_cantidad, id_producto))
            conexion.commit()

            # Imprimir la información del producto modificado
            print("\nProducto modificado:")
            print("")
            print(f"ID: {id_producto}, Nombre: {nombre}, Descripción: {descripcion}, Precio: {precio}, Categoría: {categoria}")
            print(f"Cantidad anterior: {cantidad_anterior}, Cantidad actual: {nueva_cantidad}")
            print("")
            
        salida = input("Desea modificar la cantidad de otro producto? (s/n): ").upper()
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
            SELECT cantidad, nombre, descripcion, precio, categoria FROM productos WHERE id = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("\nNo existe un producto con el ID proporcionado.\n")
        else:
            cantidad, nombre, descripcion, precio, categoria = resultado
            seguro = input(f"¿Está seguro que desea eliminar el producto:\n ID: {id_producto}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n (s/n) ").upper()
            print("")
            if seguro == "S":
                productos_eliminados.append((id_producto, nombre, descripcion, cantidad, precio, categoria))
                cursor.execute('''
                    DELETE FROM productos WHERE id = ?;
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
            id_producto, nombre, descripcion, cantidad, precio, categoria = producto
            print(f"ID: {id_producto}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}")
        print("")

    conexion.close()

def consulta_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nConsulta Datos de Productos\n")
    
    while True:
        print("\nOpciones de búsqueda:\n")
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por descripción")
        print("4. Buscar por cantidad")
        print("5. Buscar por precio")
        print("6. Buscar por categoria")
        print("")
        opcion_busqueda = int(input("Selecciona una opción (1-6): \n"))
        print("")
        print("Has seleccionado la opción de búsqueda número ", opcion_busqueda, "\n")

        match opcion_busqueda:
            case 1:  # Buscar por ID
                id_producto = int(input("Ingrese el código del producto: "))
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?;
                ''', (id_producto,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("\nNo existe un producto con el ID proporcionado.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

            case 2:  # Buscar por nombre
                nombre_producto = input("Ingrese el código del producto: ").upper()
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre = ?;
                ''', (nombre_producto,))
                resultado = cursor.fetchall()
                if resultado is None:
                    print("\nNo existe un producto con el nombre proporcionado.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

            case 3:  # Buscar por descripción
                descripcion_producto = input("Ingrese la descripción del producto: ").upper()
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE descripcion = ?;
                ''', (descripcion_producto,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("\nNo existe un producto con esa descripción.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

            case 4:  # Buscar por cantidad
                cantidad = int(input("Ingrese la cantidad del producto: "))
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad = ?;
                ''', (cantidad,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("\nNo existe un producto con esa cantidad.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

            case 5:  # Buscar por precio
                precio = float(input("Ingrese el precio del producto: "))
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE precio = ?;
                ''', (precio,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print("\nNo existe un producto con ese precio.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

            case 6:  # Buscar por categoria
                categoria_producto = input("Ingrese la categoria del producto: ").upper()
                cursor.execute('''
                    SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE categoria = ?;
                ''', (categoria_producto,))
                resultado = cursor.fetchall()
                if resultado is None:
                    print("\nNo existen productos con esa categoria.\n")
                else:
                    id, nombre, descripcion, cantidad, precio, categoria = resultado
                    print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}\n")

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

    cant_bajo_stock = int(input("Ingrese la cantidad para generar un reporte de los productos que tienen stock menor a esta cantidad: "))
    cursor.execute('''
        SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ?;
    ''', (cant_bajo_stock,))
    resultados = cursor.fetchall()

    for resultado in resultados:
        id, nombre, descripcion, cantidad, precio, categoria = resultado
        productos_bajo_stock.append((id, nombre, descripcion, cantidad, precio, categoria))

    # Imprimir los productos con bajo stock
    if productos_bajo_stock:
        print("\nProductos con bajo stock:\n")
        for producto in productos_bajo_stock:
            id, nombre, descripcion, cantidad, precio, categoria = producto
            print(f"ID: {id}, Nombre: {nombre}, Descripción: {descripcion}, Cantidad: {cantidad}, Precio: {precio}, Categoría: {categoria}")
    else:
        print("No hay productos con stock por debajo de la cantidad especificada.")

    conexion.close()
    
while True:

    mostrar_menu()
    obtener_opcion()

    match opcion:
        case 1:
            alta_productos()
        case 2:
            listado_completo()
        case 3:
            actualizar_cantidad()
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