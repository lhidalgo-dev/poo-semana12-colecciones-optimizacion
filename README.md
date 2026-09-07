# restaurante_app — Semana 12

**Estudiante:** Leython Josue Hidalgo Valdez  
**Asignatura:** Programacion Orientada a Objetos  
**Tema:** Utilización de colecciones para la mejora de rendimiento en restaurante_app  

---

## Objetivo de esta semana

Mejorar internamente la forma en que el sistema **busca, consulta y valida**
información, incorporando estructuras auxiliares en memoria (`dict` y `set`)
que reducen recorridos innecesarios sobre las listas principales.

No se agregan nuevas funcionalidades: el menú, los modelos y el servicio de
archivos permanecen sin cambios.

---

## Mejoras aplicadas (Semana 12)

Todos los cambios se realizaron en `servicios/restaurante.py`,
que es donde vive la lógica del negocio.

### 1. Índice de productos por código — `dict[str, Producto]`

| Situación | Antes (Semana 11) | Después (Semana 12) |
|-----------|-------------------|---------------------|
| `buscar_producto(codigo)` | Recorre toda `_productos` con `for` hasta encontrar coincidencia — **O(n)** | Acceso directo `_productos_por_codigo.get(codigo)` — **O(1)** |
| `registrar_producto` | Solo append a la lista | append + inserción en el dict |
| `eliminar_producto` | Solo remove de la lista | remove + `pop` del dict |

La lista `_productos` se conserva para listar, recorrer en orden y guardar en JSON.

### 2. Índice de usuarios por identificación — `dict[str, Usuario]`

| Situación | Antes (Semana 11) | Después (Semana 12) |
|-----------|-------------------|---------------------|
| `buscar_usuario(id)` | Recorre `_usuarios` con `for` — **O(n)** | `_usuarios_por_identificacion.get(id)` — **O(1)** |
| `registrar_usuario` | Solo append | append + inserción en el dict |
| `eliminar_usuario` | Solo remove | remove + `pop` del dict |

La lista `_usuarios` se conserva para listar y persistir.

### 3. Índice de ventas por usuario — `dict[str, list[Venta]]`

| Situación | Antes (Semana 11) | Después (Semana 12) |
|-----------|-------------------|---------------------|
| `consultar_ventas_usuario(id)` | Filtra `_ventas` completa con `for` — **O(n)** | Acceso directo `_ventas_por_usuario.get(id)` — **O(1)** |
| `vender_producto` | Solo append a `_ventas` | append + inserción en el dict agrupado |

La lista `_ventas` se conserva para `listar_ventas()` y la persistencia JSON.

### 4. Set de categorías activas — `set[str]`

`_categorias_activas` se actualiza al registrar, actualizar o eliminar productos.
`obtener_categorias_registradas()` devuelve la copia del set sin reconstruirlo.
Permite también validar pertenencia de categoría en **O(1)**.

### 5. Reconstrucción de índices al iniciar

El método `_reconstruir_indices()` se invoca en `__init__` después de cargar
los datos desde JSON. De esta forma, los índices reflejan exactamente el estado
persistido al abrir el programa de nuevo.

---

## Colecciones utilizadas y su responsabilidad

| Colección | Tipo | Responsabilidad |
|-----------|------|-----------------|
| `_productos` | `list` | Almacenar, recorrer en orden y persistir productos |
| `_usuarios` | `list` | Almacenar, recorrer en orden y persistir usuarios |
| `_ventas` | `list` | Almacenar, recorrer en orden y persistir ventas |
| `_productos_por_codigo` | `dict` | Búsqueda rápida de producto por código |
| `_usuarios_por_identificacion` | `dict` | Búsqueda rápida de usuario por identificación |
| `_ventas_por_usuario` | `dict` | Consulta rápida de ventas de un usuario |
| `_categorias_activas` | `set` | Categorías únicas; validación de pertenencia |

---

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py          ← único archivo modificado en Semana 12
└── main.py
```

---

## Ejecución

```bash
cd restaurante_app
python main.py
```

Requiere **Python 3.10 o superior** (se usan type hints con `|`).

---

## Pruebas realizadas

1. Ejecutar `main.py` y verificar que carga datos JSON correctamente.
2. Registrar un producto y buscarlo por código → responde en O(1).
3. Registrar un usuario y buscarlo por identificación → responde en O(1).
4. Realizar una venta y consultar ventas del usuario → resultado inmediato sin filtro lineal.
5. Actualizar y eliminar productos/usuarios → índices permanecen coherentes.
6. Cerrar y volver a abrir el programa → los índices se reconstruyen desde JSON.
7. Verificar que las categorías activas se actualicen al agregar/eliminar productos.
