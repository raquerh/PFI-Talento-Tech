'''
FUNCIONALIDADES:
    ● Registro de productos: La aplicación debe permitir al usuario agregar nuevos productos al inventario, solicitando los siguientes datos: nombre, descripción, cantidad, precio y categoría.
    ● Visualización de productos: La aplicación debe mostrar todos los productos registrados en el inventario, incluyendo su ID, nombre, descripción, cantidad, precio y categoría.
    ● Actualización de productos: La aplicación debe permitir al usuario actualizar la cantidad disponible de un producto específico utilizando su ID.
    ● Eliminación de productos: La aplicación debe permitir al usuario eliminar un producto del inventario utilizando su ID.
    ● Búsqueda de productos: La aplicación debe ofrecer una funcionalidad para buscar productos por su ID, mostrando los resultados que coincidan con los criterios de búsqueda. De manera opcional, se puede implementar la búsqueda por los campos nombre o categoría.
    ● Reporte de Bajo Stock: La aplicación debe generar un reporte de productos que tengan una cantidad igual o inferior a un límite especificado por el usuario.

'''
import colorama
from colorama import Fore, Back, Style
import sqlite3

def inicio_conexion():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    return conexion, cursor

def fin_conexion(conexion):
    conexion.commit()
    conexion.close()
    
def limpiar_color():
    print(Back.RESET + Fore.RESET)

def mostrar_menu():

    print("")
    print(Fore.YELLOW)
    print("********************************")
    print("* MENU DE GESTION DE PRODUCTOS *")
    print("********************************")
    print("")
    print("1. Alta de productos nuevos")
    print("2. Listado completo de productos")
    print("3. Actualizar el stock de un producto")
    print("4. Baja de producto")
    print("5. Consulta de productos")
    print("6. Reporte de productos con bajo stock")
    print("7. Salir\n")
    limpiar_color()

def obtener_opcion():
    while True:
        print("")
        opcion = int(input("Por favor, selecciona una opción (1-7): "))
        print("")
        if 1 <= opcion <= 7:
            return opcion
            
        else:
            print(Back.BLACK + Fore.RED + "Opción no válida. Por favor, elige una opción entre 1 y 7.")
        limpiar_color()
        
def alta_productos():
    
    conexion, cursor = inicio_conexion()
    
    print(Fore.YELLOW + "\nIngreso de nuevos productos\n")
    print("---------------------------")
    limpiar_color()

    # Lista para almacenar los productos agregados en esta sesión
    productos_agregados = []
    
    # Usamos el bucle while para ingresar los datos
    while True:
        
        NOMBRE = input("Ingresá el nombre del producto: ").upper()
        DESCRIPCION = input("Ingresá su descripcion: ").upper()
        CANTIDAD = int(input("Ingresá la cantidad del producto: "))
        PRECIO = float(input("Ingresá su precio unitario: "))
        CATEGORIA = input("Ingresá la categoria a la que pertenece: ").upper()

    # Verificar si ya existe un producto con la misma DESCRIPCION
        cursor.execute('''
            SELECT COUNT(*) FROM productos WHERE DESCRIPCION = ?;
        ''', (DESCRIPCION,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(Back.BLACK + Fore.RED + "Ya existe un producto con la misma descripcion. No se puede agregar.")
            limpiar_color()
            
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
    print(Fore.BLUE + "\nProductos ingresados en esta sesion:\n")
    
    for producto in productos_agregados:
        NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
        print(f" NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")
        
    fin_conexion(conexion)
    limpiar_color()
    
def listado_completo():
    
    conexion, cursor = inicio_conexion()
    
    cursor.execute("SELECT COUNT(*) FROM productos")
    count = cursor.fetchone()[0]
    
    if count > 0:
        # Mostrar productos
        print(Fore.YELLOW + "\nListado completo de productos:\n")
        print("------------------------------")
        limpiar_color()
        
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        for producto in productos:
            ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}")
            print("")
    else:
        # Mostrar mensaje
        print(Back.BLACK + Fore.RED + "\nNo hay productos en el inventario.\n")
    
    fin_conexion(conexion)
    limpiar_color()
    
def actualizar_cantidad():
    
    conexion, cursor = inicio_conexion()
    
    print(Fore.YELLOW + "\nActualización el stock de productos\n")
    print("-----------------------------------")
    limpiar_color()

    while True:
        # Solicitar al usuario el ID del producto y la nueva CANTIDAD
        id_producto = int(input("Ingresá el ID del producto que deseas actualizar: "))
        
        # Verificar si el ID existe y obtener la CANTIDAD anterior
        cursor.execute('''
            SELECT CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(Back.BLACK + Fore.RED + "\nNo existe un producto con el ID proporcionado.\n")
            limpiar_color()
        else:
            cantidad_anterior, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA = resultado

            # Imprimir la información del producto antes de solicitar la nueva CANTIDAD
            print(Fore.BLUE + "\nProducto seleccionado:\n")
            print(f" ID: {id_producto}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {cantidad_anterior}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")
            limpiar_color()

            # Solicitar la nueva CANTIDAD
            nueva_cantidad = int(input("Ingresá la nueva cantidad disponible: "))

            # Actualizar la CANTIDAD del producto
            cursor.execute('''
                UPDATE productos SET CANTIDAD = ? WHERE ID = ?;
            ''', (nueva_cantidad, id_producto))
            conexion.commit()

            # Imprimir la información del producto modificado
            print(Fore.LIGHTBLUE_EX + "\nProducto modificado:\n")
            print(f" ID: {id_producto}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")
            print(Fore.CYAN + f"    CANTIDAD ANTERIOR: {cantidad_anterior}\n    CANTIDAD ACTUAL: {nueva_cantidad}\n")
            limpiar_color()
            
        salida = input("Desea modificar el stock de otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break
    
    fin_conexion(conexion)
    limpiar_color()

def eliminar_producto():
    
    conexion, cursor = inicio_conexion()
    
    print(Fore.YELLOW + "\nEliminar un producto\n")
    print("--------------------")
    limpiar_color()
    
    productos_eliminados = []

    while True:
        # Solicitar el ID del producto a eliminar
        id_producto = int(input("Ingresá el ID del producto que deseas eliminar: "))
        cursor.execute('''
            SELECT CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
        ''', (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(Back.BLACK + Fore.RED + "\nNo existe un producto con el ID proporcionado.\n")
            limpiar_color()
        else:
            CANTIDAD, NOMBRE, DESCRIPCION, PRECIO, CATEGORIA = resultado
            seguro = input(Fore.RED + f"¿Está seguro que desea eliminar el producto:\n ID: {id_producto}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n \n(s/n) ").upper()
            print("")
            
            if seguro == "S":
                productos_eliminados.append((id_producto, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA))
                cursor.execute('''
                    DELETE FROM productos WHERE ID = ?;
                ''', (id_producto,))
                conexion.commit()
                print(f"Producto con ID {id_producto} eliminado correctamente.\n")
            else:
                print(Fore.GREEN + f"El producto con ID {id_producto} no fue eliminado.\n")
        limpiar_color()
        
        salida = input("¿Desea eliminar otro producto? (s/n): ").upper()
        print("")
        if salida == "N":
            break

    # Mostrar los productos eliminados en esta sesión
    if productos_eliminados:
        print(Fore.BLUE + "\nProductos eliminados en esta sesión:\n")
        for producto in productos_eliminados:
            id_producto, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f" ID: {id}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

    fin_conexion(conexion)
    limpiar_color()

def consulta_producto():
    
    conexion, cursor = inicio_conexion()
    
    print(Fore.YELLOW + "\nConsulta Datos de Productos\n")
    print("---------------------------")
    limpiar_color()
    
    while True:
        print(Fore.YELLOW + "\nOpciones de búsqueda:\n")
        print("1. Por ID")
        print("2. Por NOMBRE")
        print("3. Por DESCRIPCION")
        print("4. Por CANTIDAD")
        print("5. Por PRECIO")
        print("6. Por CATEGORIA")
        
        limpiar_color()
        
        opcion_busqueda = int(input("\nSelecciona una opción (1-6)"))

        print("Has seleccionado la opción de búsqueda número ", opcion_busqueda, "\n")

        match opcion_busqueda:
            case 1:  # Buscar por ID
                id_producto = int(input("Ingrese el codigo del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE ID = ?;
                ''', (id_producto,))
                resultado = cursor.fetchone()
                if resultado is None:
                    print(Back.BLACK + Fore.RED + "\nNo existe un producto con el ID proporcionado.\n")
                    limpiar_color()
                else:
                    ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                    print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case 2:  # Buscar por NOMBRE
                nombre_producto = input("Ingrese el nombre del producto: ").upper()
                cursor.execute('''
                    SELECT id, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(NOMBRE) LIKE ?;
                ''', (f"%{nombre_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print(Back.BLACK + Fore.RED + "\nNo hay productos con el nombre proporcionado.\n")
                    limpiar_color()
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case 3:  # Buscar por DESCRIPCION
                descripcion_producto = input("Ingrese la descripcion del producto: ").upper()
                print("")
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(DESCRIPCION) LIKE ?;
                ''', (f"%{descripcion_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print(Back.BLACK + Fore.RED + "\nNo hay productos con esa descripcion.\n")
                    limpiar_color()
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case 4:  # Buscar por CANTIDAD
                cantidad_producto = int(input("Ingrese la cantidad del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE CANTIDAD = ?;
                ''', (cantidad_producto,))
                resultados = cursor.fetchall()
                if not resultados:
                    print(Back.BLACK + Fore.RED + "\nNo hay productos con esa cantidad.\n")
                    limpiar_color()
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case 5:  # Buscar por PRECIO
                precio_producto = float(input("Ingrese el precio del producto: "))
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE PRECIO = ?;
                ''', (precio_producto,))
                resultados = cursor.fetchall()
                if not resultados:
                    print(Back.BLACK + Fore.RED + "\nNo hay productos con ese precio.\n")
                    limpiar_color()
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case 6:  # Buscar por CATEGORIA
                categoria_producto = input("Ingrese la CATEGORIA del producto: ").upper()
                cursor.execute('''
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA FROM productos WHERE UPPER(CATEGORIA) LIKE ?;
                ''', (f"%{categoria_producto}%",))
                resultados = cursor.fetchall()
                if not resultados:
                    print(Back.BLACK + Fore.RED + "\nNo hay productos con esa categoria.\n")
                    limpiar_color()
                else:
                    for resultado in resultados:
                        ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = resultado
                        print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")

            case _:  # Opción no válida
                print(Back.BLACK + Fore.RED + "Opción no válida. Por favor, elige una opción entre 1 y 6.")
                limpiar_color()

        seguir = input("¿Desea buscar otro producto? (S/N): ").upper()  # Pregunta si desea seguir buscando  
        if seguir == "N":
            break
    
    fin_conexion(conexion)
    limpiar_color()

def reporte_bajo_stock():
    
    conexion, cursor = inicio_conexion()
    
    print(Fore.YELLOW +"\nReporte de bajo stock\n")
    print("---------------------")
    limpiar_color()
    
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
        print(Fore.BLUE + f"\nProductos con stock menor a {cant_bajo_stock}\n")
        for producto in productos_bajo_stock:
            ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO, CATEGORIA = producto
            print(f" ID: {ID}\n NOMBRE: {NOMBRE}\n DESCRIPCION: {DESCRIPCION}\n CANTIDAD: {CANTIDAD}\n PRECIO: {PRECIO}\n CATEGORIA: {CATEGORIA}\n")
    else:
        print(Back.BLACK + Fore.RED + "No hay productos con stock por debajo de la CANTIDAD especificada.")
                
    fin_conexion(conexion)
    limpiar_color()
    
while True:

    mostrar_menu()
    opcion = obtener_opcion()
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
            print("")
            print(Style.BRIGHT + Fore.CYAN)
            print("***************************")
            print("*  SALIENDO DEL PROGRAMA  *")
            print("***************************\n")
            print("GRACIAS POR UTILIZAR NUESTRO SOFTWARE\n CONTROL DE STOCK - TALENTO TECH")
            limpiar_color()
            break
        case _:
            print(Back.BLACK + Fore.RED +"Opción no válida. Por favor, elige una opción entre 1 y 7.")
            limpiar_color()
