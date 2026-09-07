from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

OPCIONES_MENU: tuple[tuple[str, str], ...] = (
    ("1",  "Registrar producto"),
    ("2",  "Buscar producto"),
    ("3",  "Actualizar producto"),
    ("4",  "Eliminar producto"),
    ("5",  "Listar productos"),
    ("6",  "Registrar usuario"),
    ("7",  "Buscar usuario"),
    ("8",  "Actualizar usuario"),
    ("9",  "Eliminar usuario"),
    ("10", "Listar usuarios"),
    ("11", "Realizar venta"),
    ("12", "Consultar ventas de un usuario"),
    ("13", "Listar todas las ventas"),
    ("14", "Categorias disponibles"),
    ("0",  "Salir"),
)


def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str) -> int:
    texto = pedir_texto(mensaje)
    return int(texto)


def pedir_decimal(mensaje: str) -> float:
    texto = pedir_texto(mensaje)
    return float(texto)


def mostrar_menu() -> None:
    print("\n========== RESTAURANTE APP ==========")
    print("\nGESTION DE PRODUCTOS")
    for opcion, descripcion in OPCIONES_MENU[:5]:
        print(f"  {opcion}. {descripcion}")

    print("\nGESTION DE USUARIOS")
    for opcion, descripcion in OPCIONES_MENU[5:10]:
        print(f"  {opcion}. {descripcion}")

    print("\nOPERACIONES DE VENTA")
    for opcion, descripcion in OPCIONES_MENU[10:13]:
        print(f"  {opcion}. {descripcion}")

    print("\nCONSULTAS")
    print(f"  {OPCIONES_MENU[13][0]}. {OPCIONES_MENU[13][1]}")
    print("\n  0. Salir")
    print("=" * 38)


def guardar_productos(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_productos(restaurante.listar_productos()):
        print("Advertencia: los productos no pudieron guardarse.")


def guardar_usuarios(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_usuarios(restaurante.listar_usuarios()):
        print("Advertencia: los usuarios no pudieron guardarse.")


def guardar_ventas(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_ventas(restaurante.listar_ventas()):
        print("Advertencia: las ventas no pudieron guardarse.")


def registrar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar producto ---")
    print(f"Categorias validas: {', '.join(Producto.CATEGORIAS_VALIDAS)}")
    codigo = pedir_texto("Codigo: ")
    nombre = pedir_texto("Nombre: ")
    try:
        precio = pedir_decimal("Precio: ")
        categoria = pedir_texto("Categoria: ")
        stock = pedir_entero("Stock inicial: ")
        producto = Producto(codigo, nombre, precio, categoria, stock)
        if restaurante.registrar_producto(producto):
            print("Producto registrado correctamente.")
            guardar_productos(archivo, restaurante)
        else:
            print("El codigo ya esta registrado.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def buscar_producto(restaurante: Restaurante) -> None:
    print("\n--- Buscar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print("Producto no encontrado.")
    else:
        print(producto)


def actualizar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar producto ---")
    codigo = pedir_texto("Codigo del producto a actualizar: ")
    if restaurante.buscar_producto(codigo) is None:
        print("Producto no encontrado.")
        return
    print(f"Categorias validas: {', '.join(Producto.CATEGORIAS_VALIDAS)}")
    try:
        nuevo_nombre = pedir_texto("Nuevo nombre: ")
        nuevo_precio = pedir_decimal("Nuevo precio: ")
        nueva_categoria = pedir_texto("Nueva categoria: ")
        nuevo_stock = pedir_entero("Nuevo stock: ")
        if restaurante.actualizar_producto(codigo, nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock):
            print("Producto actualizado correctamente.")
            guardar_productos(archivo, restaurante)
        else:
            print("No se pudo actualizar el producto.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def eliminar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar producto ---")
    codigo = pedir_texto("Codigo del producto: ")
    if restaurante.eliminar_producto(codigo):
        print("Producto eliminado correctamente.")
        guardar_productos(archivo, restaurante)
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: Restaurante) -> None:
    print("\n--- Lista de productos ---")
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return
    for indice, producto in enumerate(productos):
        print(f"  {indice + 1}. {producto}")
    print(f"\nTotal: {restaurante.contar_productos()} producto(s).")


def registrar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar usuario ---")
    identificacion = pedir_texto("Identificacion: ")
    nombre = pedir_texto("Nombre: ")
    correo = pedir_texto("Correo electronico: ")
    try:
        usuario = Usuario(identificacion, nombre, correo)
        if restaurante.registrar_usuario(usuario):
            print("Usuario registrado correctamente.")
            guardar_usuarios(archivo, restaurante)
        else:
            print("La identificacion ya esta registrada.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def buscar_usuario(restaurante: Restaurante) -> None:
    print("\n--- Buscar usuario ---")
    identificacion = pedir_texto("Identificacion: ")
    usuario = restaurante.buscar_usuario(identificacion)
    if usuario is None:
        print("Usuario no encontrado.")
    else:
        print(usuario)


def actualizar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar usuario ---")
    identificacion = pedir_texto("Identificacion del usuario a actualizar: ")
    if restaurante.buscar_usuario(identificacion) is None:
        print("Usuario no encontrado.")
        return
    try:
        nuevo_nombre = pedir_texto("Nuevo nombre: ")
        nuevo_correo = pedir_texto("Nuevo correo electronico: ")
        if restaurante.actualizar_usuario(identificacion, nuevo_nombre, nuevo_correo):
            print("Usuario actualizado correctamente.")
            guardar_usuarios(archivo, restaurante)
        else:
            print("No se pudo actualizar el usuario.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def eliminar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")
    if restaurante.eliminar_usuario(identificacion):
        print("Usuario eliminado correctamente.")
        guardar_usuarios(archivo, restaurante)
    else:
        print("Usuario no encontrado.")


def listar_usuarios(restaurante: Restaurante) -> None:
    print("\n--- Lista de usuarios ---")
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for indice, usuario in enumerate(usuarios):
        print(f"  {indice + 1}. {usuario}")
    print(f"\nTotal: {len(usuarios)} usuario(s).")


def realizar_venta(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Realizar venta ---")
    identificacion = pedir_texto("Identificacion del usuario: ")
    codigo = pedir_texto("Codigo del producto: ")
    try:
        cantidad = pedir_entero("Cantidad: ")

        producto = restaurante.buscar_producto(codigo)
        if producto is not None:
            print(f"Stock disponible de '{producto.nombre}': {producto.stock}")

        if restaurante.vender_producto(codigo, identificacion, cantidad):
            producto_actualizado = restaurante.buscar_producto(codigo)
            stock_nuevo = producto_actualizado.stock if producto_actualizado else "N/D"
            print("Venta registrada correctamente.")
            print(f"Stock actualizado: {stock_nuevo}")
            guardar_ventas(archivo, restaurante)
            guardar_productos(archivo, restaurante)
        else:
            print("No se pudo realizar la venta.")
            print("Verifique: usuario y producto existentes, cantidad mayor a cero y stock suficiente.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def consultar_ventas_usuario(restaurante: Restaurante) -> None:
    print("\n--- Ventas de un usuario ---")
    identificacion = pedir_texto("Identificacion del usuario: ")

    if restaurante.buscar_usuario(identificacion) is None:
        print("Usuario no encontrado.")
        return

    ventas = restaurante.consultar_ventas_usuario(identificacion)

    if not ventas:
        print("Este usuario no tiene ventas registradas.")
        return

    print(f"Ventas registradas para '{identificacion}':")
    for indice, venta in enumerate(ventas):
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto else "Producto no disponible"
        print(
            f"  {indice + 1}. Producto: {venta.producto_codigo} ({nombre_producto}) | "
            f"Cantidad: {venta.cantidad}"
        )
    print(f"\nTotal de ventas: {len(ventas)}")


def listar_todas_ventas(restaurante: Restaurante) -> None:
    print("\n--- Todas las ventas registradas ---")
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("No hay ventas registradas.")
        return
    for indice, venta in enumerate(ventas):
        print(f"  {indice + 1}. {venta}")
    print(f"\nTotal: {restaurante.contar_ventas()} venta(s).")


def mostrar_categorias(restaurante: Restaurante) -> None:
    print("\n--- Categorias con productos registrados ---")
    categorias = restaurante.obtener_categorias_registradas()
    if not categorias:
        print("No hay categorias registradas aun.")
        return
    for categoria in sorted(categorias):
        print(f"  - {categoria}")


def main() -> None:
    archivo = ArchivoServicio()

    productos_cargados = archivo.cargar_productos()
    usuarios_cargados = archivo.cargar_usuarios()
    ventas_cargadas = archivo.cargar_ventas()

    restaurante = Restaurante(productos_cargados, usuarios_cargados, ventas_cargadas)

    print("Sistema de gestion del restaurante iniciado.")
    print(
        f"Datos recuperados: {restaurante.contar_productos()} producto(s), "
        f"{len(restaurante.listar_usuarios())} usuario(s), "
        f"{restaurante.contar_ventas()} venta(s)."
    )

    acciones: dict[str, object] = {
        "1":  lambda: registrar_producto(restaurante, archivo),
        "2":  lambda: buscar_producto(restaurante),
        "3":  lambda: actualizar_producto(restaurante, archivo),
        "4":  lambda: eliminar_producto(restaurante, archivo),
        "5":  lambda: listar_productos(restaurante),
        "6":  lambda: registrar_usuario(restaurante, archivo),
        "7":  lambda: buscar_usuario(restaurante),
        "8":  lambda: actualizar_usuario(restaurante, archivo),
        "9":  lambda: eliminar_usuario(restaurante, archivo),
        "10": lambda: listar_usuarios(restaurante),
        "11": lambda: realizar_venta(restaurante, archivo),
        "12": lambda: consultar_ventas_usuario(restaurante),
        "13": lambda: listar_todas_ventas(restaurante),
        "14": lambda: mostrar_categorias(restaurante),
    }

    while True:
        mostrar_menu()
        opcion = pedir_texto("Seleccione una opcion: ")

        if opcion == "0":
            print("Sistema cerrado. Hasta luego.")
            break

        accion = acciones.get(opcion)
        if accion is None:
            print("Opcion no valida. Intente nuevamente.")
        else:
            accion()


if __name__ == "__main__":
    main()
