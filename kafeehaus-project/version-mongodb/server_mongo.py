import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, UTC
from bson import ObjectId
import bcrypt

from database_mongo import mongodb

# Puerto único para todo
PORT = 8009  # Diferente puerto para no conflictos
HOST = '127.0.0.1'

print(f"🚀 KAFEEHAUS MONGODB - SERVIDOR EN {HOST}:{PORT}")

app = FastAPI(
    title="Kafeehaus MongoDB", 
    description="Versión con MongoDB", 
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar a MongoDB al iniciar
@app.on_event("startup")
async def startup_event():
    mongodb.connect()
    await inicializar_datos()

# Servir archivos estáticos del Front - CORREGIDO: usa la carpeta actual
app.mount("/static", StaticFiles(directory="./Front"), name="static")

# ========== FUNCIONES HELPER ==========
def get_usuario_collection():
    return mongodb.get_collection("usuarios")

def get_producto_collection():
    return mongodb.get_collection("productos")

def get_pedido_collection():
    return mongodb.get_collection("pedidos")

def get_empleado_collection():
    return mongodb.get_collection("empleados")

async def inicializar_datos():
    """Inicializar datos de prueba en MongoDB"""
    usuarios = get_usuario_collection()
    productos = get_producto_collection()
    empleados = get_empleado_collection()
    
    # Verificar si ya existen datos
    if usuarios.count_documents({}) == 0:
        # Usuarios iniciales (passwords: 123456)
        usuarios_iniciales = [
            {
                "email": "admin@cafe.cl",
                "nombre": "Administrador",
                "rol": "admin",
                "password_hash": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_creacion": datetime.now(UTC),
                "activo": True
            },
            {
                "email": "usuario@cafe.cl", 
                "nombre": "Usuario Normal",
                "rol": "usuario",
                "password_hash": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_creacion": datetime.now(UTC),
                "activo": True
            }
        ]
        usuarios.insert_many(usuarios_iniciales)
        print("✅ Usuarios iniciales creados")
    
    # ... resto del código de inicialización ...
    
    # Verificar si ya existen datos
    if usuarios.count_documents({}) == 0:
        # Usuarios iniciales (passwords: 123456)
        usuarios_iniciales = [
            {
                "email": "admin@cafe.cl",
                "nombre": "Administrador",
                "rol": "admin",
                "password_hash": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_creacion": datetime.now(UTC),
                "activo": True
            },
            {
                "email": "usuario@cafe.cl", 
                "nombre": "Usuario Normal",
                "rol": "usuario",
                "password_hash": bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_creacion": datetime.now(UTC),
                "activo": True
            }
        ]
        usuarios.insert_many(usuarios_iniciales)
        print("✅ Usuarios iniciales creados")
    
    # ... resto del código de inicialización ...
    
    if productos.count_documents({}) == 0:
        productos_iniciales = [
            {
                "nombre": "Espresso",
                "precio": 1800,
                "categoria": "bebida",
                "descripcion": "Un café intenso y aromático, perfecto para empezar el día.",
                "imagen_url": "https://via.placeholder.com/400x250?text=Espresso",
                "disponible": True,
                "fecha_creacion": datetime.now(UTC)
            },
            {
                "nombre": "Americano",
                "precio": 2000,
                "categoria": "bebida",
                "descripcion": "Café filtrado, suave y ligero, ideal para cualquier momento.",
                "imagen_url": "https://via.placeholder.com/400x250?text=Americano",
                "disponible": True,
                "fecha_creacion": datetime.now(UTC)
            },
            {
                "nombre": "Capuccino", 
                "precio": 2800,
                "categoria": "bebida",
                "descripcion": "Café espresso con leche espumosa, ideal para acompañar cualquier desayuno.",
                "imagen_url": "https://via.placeholder.com/400x250?text=Capuccino",
                "disponible": True,
                "fecha_creacion": datetime.now(UTC)
            },
            {
                "nombre": "Pie de limón",
                "precio": 1800,
                "categoria": "comida", 
                "descripcion": "Delicioso pie de limón con base crujiente y crema suave.",
                "imagen_url": "https://via.placeholder.com/400x250?text=Pie+de+Limon",
                "disponible": True,
                "fecha_creacion": datetime.now(UTC)
            }
        ]
        productos.insert_many(productos_iniciales)
        print("✅ Productos iniciales creados")
    
    if empleados.count_documents({}) == 0:
        empleados_iniciales = [
            {
                "nombre": "Ana Torres",
                "email": "ana@kafeehaus.cl",
                "rol": "Barista",
                "telefono": "+56 9 1234 5678",
                "direccion": "Av. Principal 123, Santiago",
                "fecha_contratacion": "2024-01-15",
                "salario": 450000,
                "activo": True,
                "notas": "Especialista en café de especialidad",
                "fecha_creacion": datetime.now(UTC)
            },
            {
                "nombre": "Luis Pérez",
                "email": "luis@kafeehaus.cl",
                "rol": "Cajero",
                "telefono": "+56 9 2345 6789",
                "direccion": "Calle Secundaria 456, Santiago",
                "fecha_contratacion": "2024-02-01",
                "salario": 380000,
                "activo": True,
                "notas": "Excelente trato con clientes",
                "fecha_creacion": datetime.now(UTC)
            },
            {
                "nombre": "María Gómez",
                "email": "maria@kafeehaus.cl",
                "rol": "Gerente",
                "telefono": "+56 9 3456 7890",
                "direccion": "Plaza Central 789, Santiago",
                "fecha_contratacion": "2023-11-10",
                "salario": 850000,
                "activo": True,
                "notas": "Gerente general de la sucursal",
                "fecha_creacion": datetime.now(UTC)
            }
        ]
        empleados.insert_many(empleados_iniciales)
        print("✅ Empleados iniciales creados")

# ========== API ENDPOINTS ==========

# AUTH
@app.post("/api/auth/login")
async def login(request: Request):
    try:
        data = await request.json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        print(f"🔐 Login MongoDB: {email}")
        
        usuario = get_usuario_collection().find_one({"email": email})
        
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
            return {
                "mensaje": "Login exitoso",
                "rol": usuario['rol'],
                "email": usuario['email'],
                "nombre": usuario['nombre']
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error del servidor"
        )

# PRODUCTOS - ENDPOINTS COMPLETOS Y CORREGIDOS
@app.get("/api/productos")
async def get_productos():
    try:
        productos = list(get_producto_collection().find().sort("fecha_creacion", -1))
        # Convertir ObjectId a string para JSON
        for producto in productos:
            producto['id'] = str(producto['_id'])
            del producto['_id']
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/productos/{producto_id}")
async def get_producto(producto_id: str):
    try:
        producto = get_producto_collection().find_one({"_id": ObjectId(producto_id)})
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Convertir ObjectId a string
        producto['id'] = str(producto['_id'])
        del producto['_id']
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/productos")
async def crear_producto(request: Request):
    try:
        data = await request.json()
        data['fecha_creacion'] = datetime.now(UTC)
        
        # Validar campos requeridos
        campos_requeridos = ['nombre', 'precio', 'categoria', 'imagen_url', 'descripcion']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                raise HTTPException(status_code=400, detail=f"Campo requerido: {campo}")
        
        # Asegurar que 'disponible' tenga valor por defecto
        if 'disponible' not in data:
            data['disponible'] = True
        
        # Insertar producto
        result = get_producto_collection().insert_one(data)
        return {
            "mensaje": "Producto creado exitosamente", 
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/productos/{producto_id}")
async def actualizar_producto(producto_id: str, request: Request):
    try:
        data = await request.json()
        
        # Verificar que el producto existe
        producto_existente = get_producto_collection().find_one({"_id": ObjectId(producto_id)})
        if not producto_existente:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Actualizar producto
        result = get_producto_collection().update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el producto")
            
        return {"mensaje": "Producto actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/productos/{producto_id}")
async def eliminar_producto(producto_id: str):
    try:
        result = get_producto_collection().delete_one({"_id": ObjectId(producto_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PEDIDOS
@app.post("/api/pedidos")
async def crear_pedido(request: Request):
    try:
        data = await request.json()
        data['fecha_creacion'] = datetime.now(UTC)
        data['estado'] = 'pendiente'
        
        # Validar campos requeridos
        if 'usuario_email' not in data or not data['usuario_email']:
            raise HTTPException(status_code=400, detail="Email de usuario requerido")
        
        if 'items' not in data or not data['items']:
            raise HTTPException(status_code=400, detail="El pedido debe contener items")
        
        # Calcular total si no viene
        if 'total' not in data:
            data['total'] = sum(item.get('precio', 0) * item.get('cantidad', 1) for item in data['items'])
        
        result = get_pedido_collection().insert_one(data)
        
        print(f"🛒 Pedido MongoDB creado: {data.get('usuario_email')} - Total: ${data.get('total')}")
        
        return {
            "mensaje": "Pedido creado exitosamente", 
            "id_pedido": str(result.inserted_id),
            "total": data.get('total', 0)
        }
    except Exception as e:
        print(f"❌ Error creando pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pedidos")
async def obtener_pedidos():
    try:
        pedidos = list(get_pedido_collection().find().sort("fecha_creacion", -1))
        for pedido in pedidos:
            pedido['id'] = str(pedido['_id'])
            del pedido['_id']
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pedidos/{pedido_id}")
async def obtener_pedido(pedido_id: str):
    try:
        pedido = get_pedido_collection().find_one({"_id": ObjectId(pedido_id)})
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        pedido['id'] = str(pedido['_id'])
        del pedido['_id']
        return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/pedidos/{pedido_id}")
async def actualizar_estado_pedido(pedido_id: str, request: Request):
    try:
        data = await request.json()
        nuevo_estado = data.get('estado')
        
        if nuevo_estado not in ['pendiente', 'completado', 'cancelado']:
            raise HTTPException(status_code=400, detail="Estado inválido")
        
        result = get_pedido_collection().update_one(
            {"_id": ObjectId(pedido_id)},
            {"$set": {"estado": nuevo_estado}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
            
        return {"mensaje": f"Pedido actualizado a {nuevo_estado}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# EMPLEADOS - ENDPOINTS COMPLETOS
@app.get("/api/admin/empleados")
async def get_empleados():
    try:
        empleados = list(get_empleado_collection().find().sort("nombre", 1))
        for empleado in empleados:
            empleado['id'] = str(empleado['_id'])
            del empleado['_id']
        return empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/empleados/{empleado_id}")
async def get_empleado(empleado_id: str):
    try:
        empleado = get_empleado_collection().find_one({"_id": ObjectId(empleado_id)})
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        empleado['id'] = str(empleado['_id'])
        del empleado['_id']
        return empleado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/empleados")
async def crear_empleado(request: Request):
    try:
        data = await request.json()
        data['fecha_creacion'] = datetime.now(UTC)
        
        # Validar campos requeridos
        campos_requeridos = ['nombre', 'email', 'rol']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                raise HTTPException(status_code=400, detail=f"Campo requerido: {campo}")
        
        # Verificar si el email ya existe
        empleado_existente = get_empleado_collection().find_one({"email": data['email']})
        if empleado_existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        # Asegurar que 'activo' tenga valor por defecto
        if 'activo' not in data:
            data['activo'] = True
        
        # Establecer fecha de contratación por defecto si no viene
        if 'fecha_contratacion' not in data or not data['fecha_contratacion']:
            data['fecha_contratacion'] = datetime.now(UTC).strftime('%Y-%m-%d')
        
        result = get_empleado_collection().insert_one(data)
        return {
            "mensaje": "Empleado creado exitosamente", 
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/empleados/{empleado_id}")
async def actualizar_empleado(empleado_id: str, request: Request):
    try:
        data = await request.json()
        
        # Verificar que el empleado existe
        empleado_existente = get_empleado_collection().find_one({"_id": ObjectId(empleado_id)})
        if not empleado_existente:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        # Si se está actualizando el email, verificar que no exista otro empleado con el mismo email
        if 'email' in data and data['email'] != empleado_existente.get('email'):
            email_existente = get_empleado_collection().find_one({
                "email": data['email'],
                "_id": {"$ne": ObjectId(empleado_id)}
            })
            if email_existente:
                raise HTTPException(status_code=400, detail="El email ya está registrado por otro empleado")
        
        # Actualizar empleado
        result = get_empleado_collection().update_one(
            {"_id": ObjectId(empleado_id)},
            {"$set": data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el empleado")
            
        return {"mensaje": "Empleado actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/empleados/{empleado_id}")
async def eliminar_empleado(empleado_id: str):
    try:
        result = get_empleado_collection().delete_one({"_id": ObjectId(empleado_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return {"mensaje": "Empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint adicional para cambiar estado de empleado
@app.patch("/api/admin/empleados/{empleado_id}/estado")
async def cambiar_estado_empleado(empleado_id: str, request: Request):
    try:
        data = await request.json()
        nuevo_estado = data.get('activo')
        
        if nuevo_estado is None:
            raise HTTPException(status_code=400, detail="El campo 'activo' es requerido")
        
        result = get_empleado_collection().update_one(
            {"_id": ObjectId(empleado_id)},
            {"$set": {"activo": nuevo_estado}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
            
        estado_texto = "activado" if nuevo_estado else "desactivado"
        return {"mensaje": f"Empleado {estado_texto} exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# REPORTES
@app.get("/api/admin/reportes/ventas")
async def get_reportes_ventas():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_ventas": {"$sum": "$total"},
                    "total_pedidos": {"$sum": 1},
                    "pedidos_completados": {
                        "$sum": {"$cond": [{"$eq": ["$estado", "completado"]}, 1, 0]}
                    },
                    "pedidos_pendientes": {
                        "$sum": {"$cond": [{"$eq": ["$estado", "pendiente"]}, 1, 0]}
                    }
                }
            }
        ]
        
        result = list(get_pedido_collection().aggregate(pipeline))
        
        if result:
            reporte = result[0]
            # Eliminar el _id del resultado
            if '_id' in reporte:
                del reporte['_id']
            return reporte
        else:
            return {
                "total_ventas": 0,
                "total_pedidos": 0,
                "pedidos_completados": 0,
                "pedidos_pendientes": 0
            }
    except Exception as e:
        print(f"❌ Error en reportes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NUEVO ENDPOINT: REPORTE DE VENTAS POR DÍA
@app.get("/api/admin/reportes/ventas-dia")
async def get_reportes_ventas_dia(fecha: str):
    try:
        # Convertir la fecha string a datetime
        fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_fin = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 23, 59, 59)
        
        print(f"📊 Generando reporte para fecha: {fecha}")
        
        # Pipeline para obtener pedidos del día específico
        pipeline = [
            {
                "$match": {
                    "fecha_creacion": {
                        "$gte": fecha_inicio,
                        "$lte": fecha_fin
                    }
                }
            },
            {
                "$sort": {"fecha_creacion": -1}
            }
        ]
        
        pedidos = list(get_pedido_collection().aggregate(pipeline))
        
        if not pedidos:
            raise HTTPException(status_code=404, detail="No existen ventas registradas en el período seleccionado")
        
        # Convertir ObjectId a string para JSON
        for pedido in pedidos:
            pedido['id'] = str(pedido['_id'])
            del pedido['_id']
        
        # Calcular estadísticas
        total_ventas = sum(pedido.get('total', 0) for pedido in pedidos)
        total_pedidos = len(pedidos)
        pedidos_completados = sum(1 for pedido in pedidos if pedido.get('estado') == 'completado')
        pedidos_pendientes = total_pedidos - pedidos_completados
        
        return {
            "fecha": fecha,
            "total_ventas": total_ventas,
            "total_pedidos": total_pedidos,
            "pedidos_completados": pedidos_completados,
            "pedidos_pendientes": pedidos_pendientes,
            "pedidos": pedidos
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en reporte por día: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/reportes/productos-populares")
async def get_productos_populares():
    try:
        pipeline = [
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": "$items.nombre",
                    "total_vendido": {"$sum": "$items.cantidad"},
                    "ingresos_totales": {"$sum": {"$multiply": ["$items.precio", "$items.cantidad"]}}
                }
            },
            {"$sort": {"total_vendido": -1}},
            {"$limit": 10}
        ]
        
        productos_populares = list(get_pedido_collection().aggregate(pipeline))
        
        # Formatear resultado
        resultado = []
        for producto in productos_populares:
            resultado.append({
                "nombre": producto["_id"],
                "total_vendido": producto["total_vendido"],
                "ingresos_totales": producto["ingresos_totales"]
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# REPORTE DE EMPLEADOS
@app.get("/api/admin/reportes/empleados")
async def get_reporte_empleados():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$rol",
                    "total_empleados": {"$sum": 1},
                    "empleados_activos": {
                        "$sum": {"$cond": [{"$eq": ["$activo", True]}, 1, 0]}
                    },
                    "empleados_inactivos": {
                        "$sum": {"$cond": [{"$eq": ["$activo", False]}, 1, 0]}
                    }
                }
            },
            {"$sort": {"total_empleados": -1}}
        ]
        
        reporte_empleados = list(get_empleado_collection().aggregate(pipeline))
        
        # Formatear resultado
        resultado = []
        for rol in reporte_empleados:
            resultado.append({
                "rol": rol["_id"],
                "total_empleados": rol["total_empleados"],
                "empleados_activos": rol["empleados_activos"],
                "empleados_inactivos": rol["empleados_inactivos"]
            })
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# HEALTH CHECK
@app.get("/api/health")
async def health():
    try:
        # Verificar conexión a MongoDB
        mongodb.client.admin.command('ping')
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy", 
        "message": "Kafeehaus MongoDB API",
        "database": db_status,
        "timestamp": datetime.now(UTC).isoformat()
    }
# Añadir este endpoint al server_mongo.py existente

# AUTH - NUEVO ENDPOINT DE REGISTRO
@app.post("/api/auth/register")
async def register(request: Request):
    try:
        data = await request.json()
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        print(f"👤 Registrando nuevo usuario: {email}")
        
        # Validar campos requeridos
        if not nombre or not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos"
            )
        
        # Validar formato de email
        if '@' not in email or '.' not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de email inválido"
            )
        
        # Validar longitud de contraseña
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 6 caracteres"
            )
        
        # Verificar si el email ya existe
        usuarios = get_usuario_collection()
        usuario_existente = usuarios.find_one({"email": email})
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear hash de la contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Crear nuevo usuario (rol por defecto: 'usuario')
        nuevo_usuario = {
            "nombre": nombre,
            "email": email,
            "password_hash": password_hash,
            "rol": "usuario",  # Rol por defecto
            "fecha_creacion": datetime.now(UTC),
            "activo": True
        }
        
        # Insertar en la base de datos
        result = usuarios.insert_one(nuevo_usuario)
        
        print(f"✅ Usuario registrado exitosamente: {email}")
        
        return {
            "mensaje": "Usuario registrado exitosamente",
            "email": email,
            "nombre": nombre,
            "rol": "usuario"
        }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error del servidor al registrar usuario"
        )

# ========== SERVIR PÁGINAS HTML ==========
@app.get("/")
async def home():
    return FileResponse("./Front/FrontFinal.html")

@app.get("/iniciarsesion")
async def login_page():
    return FileResponse("./Front/IniciarSesion.html")

@app.get("/menu")
async def menu_page():
    return FileResponse("./Front/Menu.html")

@app.get("/adminpanel")
async def admin_page():
    return FileResponse("./Front/AdminPanel.html")

@app.get("/pago")
async def payment_page():
    return FileResponse("./Front/Pago.html")

@app.get("/carrito")
async def cart_page():
    return FileResponse("./Front/carrito.html")

# Manejo de errores global
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint no encontrado"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# Añadir este endpoint al server_mongo.py existente

# AUTH - NUEVO ENDPOINT DE REGISTRO
@app.post("/api/auth/register")
async def register(request: Request):
    try:
        data = await request.json()
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        print(f"👤 Registrando nuevo usuario: {email}")
        
        # Validar campos requeridos
        if not nombre or not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todos los campos son requeridos"
            )
        
        # Validar formato de email
        if '@' not in email or '.' not in email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de email inválido"
            )
        
        # Validar longitud de contraseña
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 6 caracteres"
            )
        
        # Verificar si el email ya existe
        usuarios = get_usuario_collection()
        usuario_existente = usuarios.find_one({"email": email})
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear hash de la contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Crear nuevo usuario (rol por defecto: 'usuario')
        nuevo_usuario = {
            "nombre": nombre,
            "email": email,
            "password_hash": password_hash,
            "rol": "usuario",  # Rol por defecto
            "fecha_creacion": datetime.now(UTC),
            "activo": True
        }
        
        # Insertar en la base de datos
        result = usuarios.insert_one(nuevo_usuario)
        
        print(f"✅ Usuario registrado exitosamente: {email}")
        
        return {
            "mensaje": "Usuario registrado exitosamente",
            "email": email,
            "nombre": nombre,
            "rol": "usuario"
        }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error del servidor al registrar usuario"
        )

# CONFIGURACIÓN PARA FORZAR PUERTO
if __name__ == "__main__":
    print("=" * 50)
    print(f"🌐 KAFEEHAUS MONGODB: http://{HOST}:{PORT}")
    print(f"🔐 LOGIN: http://{HOST}:{PORT}/iniciarsesion")
    print(f"📋 MENÚ: http://{HOST}:{PORT}/menu")
    print(f"⚙️  ADMIN: http://{HOST}:{PORT}/adminpanel")
    print(f"📚 API DOCS: http://{HOST}:{PORT}/docs")
    print("=" * 50)
    print("🗄️  Base de datos: MongoDB")
    print("👤 Credenciales de prueba:")
    print("   - Admin: admin@cafe.cl / 123456")
    print("   - Usuario: usuario@cafe.cl / 123456")
    print("=" * 50)
    print("📊 Nueva función: Reportes de ventas por día disponible")
    print("=" * 50)
    
    uvicorn.run(app, host=HOST, port=PORT, reload=False)