from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        # Las listas principales se conservan para recorrer, listar y persistir objetos.
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = usuarios_iniciales.copy() if usuarios_iniciales else []
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

        # MEJORA SEMANA 12: índices auxiliares en memoria para búsquedas frecuentes.
        # Los diccionarios permiten localizar productos y usuarios por clave sin recorrer
        # toda la lista, pasando de O(n) a O(1) en las búsquedas más usadas.
        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}

        # MEJORA SEMANA 12: agrupación de ventas por usuario para consultas rápidas.
        # En lugar de filtrar toda la lista cada vez, accedemos directamente por clave.
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

        # MEJORA SEMANA 12: set de categorías activas para validación de pertenencia.
        # Un set permite verificar si una categoría tiene productos en O(1).
        self._categorias_activas: set[str] = set()

        # Reconstruir los índices desde los datos cargados (JSON).
        self._reconstruir_indices()

    # ------------------------------------------------------------------
    # Reconstrucción de índices
    # ------------------------------------------------------------------

    def _reconstruir_indices(self) -> None:
        """Reconstruye todas las estructuras auxiliares a partir de las listas principales.

        Se invoca al iniciar el programa, después de cargar los datos desde JSON,
        para que los índices reflejen exactamente el estado persistido.
        """
        self._productos_por_codigo = {}
        self._usuarios_por_identificacion = {}
        self._ventas_por_usuario = {}
        self._categorias_activas = set()

        for producto in self._productos:
            self._productos_por_codigo[producto.codigo] = producto
            self._categorias_activas.add(producto.categoria)

        for usuario in self._usuarios:
            self._usuarios_por_identificacion[usuario.identificacion] = usuario

        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    # ------------------------------------------------------------------
    # Gestión de productos
    # ------------------------------------------------------------------

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False
        self._productos.append(producto)
        # Sincronizar índices al registrar.
        self._productos_por_codigo[producto.codigo] = producto
        self._categorias_activas.add(producto.categoria)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        # MEJORA SEMANA 12: búsqueda directa por clave en dict (O(1)).
        # Antes se recorría toda la lista con un bucle for.
        codigo = codigo.strip().upper()
        return self._productos_por_codigo.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str,
        nuevo_precio: float,
        nueva_categoria: str,
        nuevo_stock: int,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        producto.categoria = nueva_categoria
        producto.stock = nuevo_stock
        # Reconstruir el set de categorías activas porque puede haber cambiado.
        self._categorias_activas = {p.categoria for p in self._productos}
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        # Sincronizar índices al eliminar.
        self._productos_por_codigo.pop(producto.codigo, None)
        self._categorias_activas = {p.categoria for p in self._productos}
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def obtener_categorias_registradas(self) -> set[str]:
        # MEJORA SEMANA 12: el set se mantiene actualizado; no se recalcula aquí.
        return self._categorias_activas.copy()

    # ------------------------------------------------------------------
    # Gestión de usuarios
    # ------------------------------------------------------------------

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        # Sincronizar índice al registrar.
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        # MEJORA SEMANA 12: búsqueda directa por clave (O(1)).
        # Antes se recorría toda la lista con un bucle for.
        identificacion = identificacion.strip()
        return self._usuarios_por_identificacion.get(identificacion)

    def actualizar_usuario(
        self,
        identificacion: str,
        nuevo_nombre: str,
        nuevo_correo: str,
    ) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        usuario.nombre = nuevo_nombre
        usuario.correo = nuevo_correo
        # El índice apunta al mismo objeto; no necesita actualizarse.
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        # Sincronizar índice al eliminar.
        self._usuarios_por_identificacion.pop(usuario.identificacion, None)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    # ------------------------------------------------------------------
    # Ventas
    # ------------------------------------------------------------------

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        # MEJORA SEMANA 12: actualizar el índice de ventas por usuario al registrar.
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)
        producto.vender(cantidad)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        # MEJORA SEMANA 12: consulta directa por clave en el índice (O(1)).
        # Antes se recorría toda la lista _ventas buscando coincidencias.
        identificacion_usuario = identificacion_usuario.strip()
        return self._ventas_por_usuario.get(identificacion_usuario, []).copy()

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def contar_ventas(self) -> int:
        return len(self._ventas)
