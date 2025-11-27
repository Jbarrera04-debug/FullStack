import bcrypt
from datetime import datetime, UTC
from database_mongo import mongodb

def agregar_productos():
    productos = mongodb.get_collection("productos")
    
    # Lista de productos a agregar
    nuevos_productos = [
        # === BEBIDAS CALIENTES ===
        {
            "nombre": "Espresso Doble",
            "precio": 2200,
            "categoria": "bebida",
            "descripcion": "Doble shot de espresso para más intensidad y sabor.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Espresso+Doble",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Macchiato",
            "precio": 2400,
            "categoria": "bebida", 
            "descripcion": "Espresso con una pequeña cantidad de leche espumada.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Macchiato",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Mocha",
            "precio": 3200,
            "categoria": "bebida",
            "descripcion": "Deliciosa combinación de espresso, chocolate y leche vaporizada.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Mocha",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Flat White",
            "precio": 2800,
            "categoria": "bebida",
            "descripcion": "Espresso suave con leche microespumada cremosa.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Flat+White",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Café con Leche",
            "precio": 2000,
            "categoria": "bebida",
            "descripcion": "Clásico café con leche, perfecto para cualquier momento del día.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Cafe+Leche",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Té Negro",
            "precio": 1500,
            "categoria": "bebida",
            "descripcion": "Té negro de calidad premium, aromático y reconfortante.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Te+Negro",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Té Verde",
            "precio": 1600,
            "categoria": "bebida",
            "descripcion": "Té verde natural con antioxidantes, suave y refrescante.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Te+Verde",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Té de Frutos Rojos",
            "precio": 1800,
            "categoria": "bebida",
            "descripcion": "Infusión de frutos rojos con un toque dulce natural.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Te+Frutos+Rojos",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Chocolate Caliente",
            "precio": 2500,
            "categoria": "bebida",
            "descripcion": "Chocolate caliente cremoso con cocoa premium.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Chocolate+Caliente",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },

        # === BEBIDAS FRÍAS ===
        {
            "nombre": "Iced Coffee",
            "precio": 2800,
            "categoria": "bebida_fria",
            "descripcion": "Café frío suave con hielo, refrescante y vigorizante.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Iced+Coffee",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Frappé",
            "precio": 3500,
            "categoria": "bebida_fria",
            "descripcion": "Bebida mezclada con café, hielo y crema batida.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Frappe",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Cold Brew",
            "precio": 3000,
            "categoria": "bebida_fria",
            "descripcion": "Café infusionado en frío por 12 horas, suave y menos ácido.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Cold+Brew",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Limonada Natural",
            "precio": 2200,
            "categoria": "bebida_fria",
            "descripcion": "Limonada fresca con limones naturales y hielo.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Limonada+Natural",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Jugo de Naranja Natural",
            "precio": 2500,
            "categoria": "bebida_fria",
            "descripcion": "Jugo de naranja recién exprimido, lleno de vitamina C.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Jugo+Naranja",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },

        # === REPOSTERÍA ===
        {
            "nombre": "Croissant de Jamón y Queso",
            "precio": 3200,
            "categoria": "comida",
            "descripcion": "Croissant relleno de jamón y queso derretido.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Croissant+Jamon+Queso",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Medialuna",
            "precio": 1200,
            "categoria": "comida",
            "descripcion": "Medialuna dulce y esponjosa, perfecta para acompañar el café.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Medialuna",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Alfajor",
            "precio": 1800,
            "categoria": "comida",
            "descripcion": "Dos galletas rellenas de dulce de leche y bañadas en chocolate.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Alfajor",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Cheesecake",
            "precio": 3800,
            "categoria": "comida",
            "descripcion": "Tarta de queso cremosa con base de galleta.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Cheesecake",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Tiramisú",
            "precio": 3500,
            "categoria": "comida",
            "descripcion": "Postre italiano con café, cacao y queso mascarpone.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Tiramisu",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Muffin de Arándanos",
            "precio": 2200,
            "categoria": "comida",
            "descripcion": "Muffin esponjoso con arándanos frescos.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Muffin+Arandanos",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Galletas de Avena",
            "precio": 1500,
            "categoria": "comida",
            "descripcion": "Galletas saludables de avena con pasas y miel.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Galletas+Avena",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Torta de Chocolate",
            "precio": 2800,
            "categoria": "comida",
            "descripcion": "Porción de torta de chocolate intenso y cremosa.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Torta+Chocolate",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Panini Caprese",
            "precio": 4200,
            "categoria": "comida",
            "descripcion": "Sandwich tostado con mozzarella, tomate y albahaca.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Panini+Caprese",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Bagel con Queso Crema",
            "precio": 2800,
            "categoria": "comida",
            "descripcion": "Bagel fresco con queso crema suave.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Bagel+Queso+Crema",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Ensalada César",
            "precio": 4800,
            "categoria": "comida",
            "descripcion": "Ensalada fresca con lechuga, pollo, crutones y aderezo césar.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Ensalada+Cesar",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Quiche de Espinacas",
            "precio": 3200,
            "categoria": "comida",
            "descripcion": "Tarta salada con espinacas, huevo y queso.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Quiche+Espinacas",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        },
        {
            "nombre": "Sándwich Club",
            "precio": 4500,
            "categoria": "comida",
            "descripcion": "Sándwich triple con pollo, tocino, lechuga y tomate.",
            "imagen_url": "https://via.placeholder.com/400x250?text=Sandwich+Club",
            "disponible": True,
            "fecha_creacion": datetime.now(UTC)
        }
    ]
    
    # Insertar productos
    result = productos.insert_many(nuevos_productos)
    print(f"✅ {len(result.inserted_ids)} productos agregados exitosamente!")
    
    # Mostrar resumen
    categorias = productos.distinct("categoria")
    for categoria in categorias:
        count = productos.count_documents({"categoria": categoria})
        print(f"   - {categoria}: {count} productos")

if __name__ == "__main__":
    mongodb.connect()
    agregar_productos()
    mongodb.close()