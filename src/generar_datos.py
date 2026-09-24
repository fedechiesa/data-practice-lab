from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import random
import re

import pandas as pd


@dataclass(frozen=True)
class ConfiguracionDatos:
    semilla: int = 42
    cantidad_clientes: int = 1000
    cantidad_pedidos: int = 8000
    cantidad_productos: int = 100
    fecha_inicio_pedidos: date = date(2024, 1, 1)
    fecha_fin_pedidos: date = date(2026, 8, 31)


CATEGORIAS = [
    (1, "Vinos Tintos", "Vinos tintos de distintas variedades"),
    (2, "Vinos Blancos", "Vinos blancos jovenes y reserva"),
    (3, "Vinos Rosados", "Vinos rosados frescos"),
    (4, "Espumantes", "Espumantes y vinos espumosos"),
    (5, "Whisky", "Whiskies nacionales e importados"),
    (6, "Gin", "Gins nacionales e importados"),
    (7, "Vodka", "Vodkas nacionales e importados"),
    (8, "Aperitivos", "Aperitivos, vermut y bitter"),
    (9, "Cervezas", "Cervezas artesanales y premium"),
    (10, "Accesorios", "Copas, destapadores y accesorios"),
]

CATEGORIA_DEMANDA = {
    1: 1.45,
    2: 1.05,
    3: 0.65,
    4: 1.25,
    5: 0.90,
    6: 1.10,
    7: 0.60,
    8: 0.75,
    9: 0.85,
    10: 0.45,
}

MARGEN_CATEGORIA = {
    1: (0.58, 0.70),
    2: (0.56, 0.68),
    3: (0.55, 0.67),
    4: (0.52, 0.65),
    5: (0.68, 0.80),
    6: (0.50, 0.63),
    7: (0.54, 0.66),
    8: (0.48, 0.62),
    9: (0.57, 0.72),
    10: (0.38, 0.55),
}

MARCAS = [
    "Altos del Sol",
    "Bodega Norte",
    "Casa Andina",
    "Finca Sur",
    "La Reserva",
    "Monte Claro",
    "Patagonia Select",
    "Rio Seco",
    "Valle Azul",
    "Viña Central",
]

PROVINCIAS_BASE = [
    "Buenos Aires",
    "CABA",
    "Cordoba",
    "Santa Fe",
    "Mendoza",
    "Neuquen",
    "Rio Negro",
    "Entre Rios",
    "Tucuman",
    "Salta",
]

VARIANTES_PROVINCIA = {
    "CABA": ["CABA", "Capital Federal", "caba", "Ciudad Autonoma de Buenos Aires"],
    "Cordoba": ["Cordoba", "cordoba", "Córdoba"],
    "Buenos Aires": ["Buenos Aires", "Bs As", "BUENOS AIRES"],
}

NOMBRES = [
    "Agustina",
    "Camila",
    "Carla",
    "Diego",
    "Federico",
    "Florencia",
    "Gonzalo",
    "Julieta",
    "Laura",
    "Lucia",
    "Manuel",
    "Mariana",
    "Martin",
    "Natalia",
    "Pablo",
    "Santiago",
    "Sofia",
    "Valentina",
]

APELLIDOS = [
    "Acosta",
    "Alvarez",
    "Benitez",
    "Castro",
    "Diaz",
    "Fernandez",
    "Garcia",
    "Gomez",
    "Lopez",
    "Martinez",
    "Pereyra",
    "Ramirez",
    "Rodriguez",
    "Sanchez",
    "Silva",
]

CANALES = ["Web", "Tienda fisica", "App", "Marketplace", "WhatsApp"]
METODOS_PAGO = ["Tarjeta credito", "Tarjeta debito", "Transferencia", "Mercado Pago", "Efectivo"]


def generar_datos(config: ConfiguracionDatos | None = None) -> dict[str, pd.DataFrame]:
    """Genera todos los DataFrames respetando integridad referencial."""
    config = config or ConfiguracionDatos()
    rnd = random.Random(config.semilla)

    categorias = _generar_categorias()
    productos = _generar_productos(rnd, config.cantidad_productos)
    clientes = _generar_clientes(rnd, config.cantidad_clientes, config.fecha_fin_pedidos)
    pedidos = _generar_pedidos(rnd, config, clientes)
    detalle_pedido = _generar_detalle_pedido(rnd, pedidos, productos)
    pagos = _generar_pagos(rnd, pedidos, detalle_pedido)
    movimientos_stock = _generar_movimientos_stock(rnd, productos, detalle_pedido, pedidos)

    return {
        "categorias": categorias,
        "productos": productos.drop(columns=["peso_demanda"]),
        "clientes": clientes,
        "pedidos": pedidos,
        "detalle_pedido": detalle_pedido,
        "pagos": pagos,
        "movimientos_stock": movimientos_stock,
    }


def guardar_csv(datasets: dict[str, pd.DataFrame], carpeta: str | Path = "data/raw") -> None:
    ruta = Path(carpeta)
    ruta.mkdir(parents=True, exist_ok=True)

    for nombre, dataframe in datasets.items():
        dataframe.to_csv(ruta / f"{nombre}.csv", index=False, encoding="utf-8")


def _generar_categorias() -> pd.DataFrame:
    return pd.DataFrame(CATEGORIAS, columns=["categoria_id", "nombre", "descripcion"])


def _generar_productos(rnd: random.Random, cantidad_productos: int) -> pd.DataFrame:
    productos = []
    nombres_por_categoria = {
        1: ["Malbec", "Cabernet Sauvignon", "Pinot Noir", "Blend Tinto", "Syrah"],
        2: ["Chardonnay", "Sauvignon Blanc", "Torrontes", "Blend Blanco"],
        3: ["Rosado Malbec", "Rose Pinot", "Rosado Dulce"],
        4: ["Extra Brut", "Brut Nature", "Demi Sec", "Rose Espumante"],
        5: ["Single Malt", "Blend Scotch", "Bourbon", "Irish Whiskey"],
        6: ["London Dry", "Gin Botanico", "Pink Gin", "Gin Citrus"],
        7: ["Vodka Clasico", "Vodka Premium", "Vodka Citrus"],
        8: ["Vermut Rosso", "Vermut Bianco", "Aperitivo Bitter"],
        9: ["IPA", "Honey", "Porter", "Golden Ale"],
        10: ["Copa Cristal", "Destapador", "Decanter", "Set Regalo"],
    }

    categorias = [categoria_id for categoria_id, _, _ in CATEGORIAS]
    for producto_id in range(1, cantidad_productos + 1):
        categoria_id = categorias[(producto_id - 1) % len(categorias)]
        nombre_base = rnd.choice(nombres_por_categoria[categoria_id])
        marca = rnd.choice(MARCAS)
        tier = rnd.choices(["popular", "medio", "baja_rotacion"], weights=[0.25, 0.55, 0.20], k=1)[0]

        precio_base = _precio_base_categoria(rnd, categoria_id)
        if tier == "popular":
            precio = precio_base * rnd.uniform(0.85, 1.10)
            stock = rnd.randint(80, 220)
            peso_demanda = rnd.uniform(1.6, 2.5)
        elif tier == "baja_rotacion":
            precio = precio_base * rnd.uniform(1.05, 1.45)
            stock = rnd.randint(5, 45)
            peso_demanda = rnd.uniform(0.15, 0.55)
        else:
            precio = precio_base * rnd.uniform(0.95, 1.25)
            stock = rnd.randint(30, 120)
            peso_demanda = rnd.uniform(0.7, 1.3)

        if rnd.random() < 0.015:
            precio *= rnd.uniform(2.5, 4.0)  # outlier plausible: producto premium.

        costo_min, costo_max = MARGEN_CATEGORIA[categoria_id]
        costo = precio * rnd.uniform(costo_min, costo_max)

        productos.append(
            {
                "producto_id": producto_id,
                "nombre": f"{nombre_base} {marca} {750 if categoria_id <= 8 else rnd.choice([1, 2, 6])}",
                "categoria_id": categoria_id,
                "marca": marca,
                "precio": round(precio, 2),
                "costo": round(costo, 2),
                "stock": stock,
                "peso_demanda": round(peso_demanda * CATEGORIA_DEMANDA[categoria_id], 4),
            }
        )

    return pd.DataFrame(productos)


def _generar_clientes(rnd: random.Random, cantidad_clientes: int, fecha_fin: date) -> pd.DataFrame:
    clientes = []
    segmentos = rnd.choices(
        ["alto_valor", "frecuente", "ocasional", "inactivo"],
        weights=[0.05, 0.20, 0.60, 0.15],
        k=cantidad_clientes,
    )

    for cliente_id, segmento in enumerate(segmentos, start=1):
        nombre = f"{rnd.choice(NOMBRES)} {rnd.choice(APELLIDOS)}"
        provincia = _provincia_con_variacion(rnd)
        fecha_registro = _fecha_aleatoria(rnd, date(2022, 1, 1), fecha_fin - timedelta(days=20))
        slug = _slug(nombre)
        email = f"{slug}.{cliente_id:04d}@example.com"

        if rnd.random() < 0.025:
            nombre = nombre.upper()
        elif rnd.random() < 0.025:
            nombre = nombre.lower()

        clientes.append(
            {
                "cliente_id": cliente_id,
                "nombre": nombre,
                "email": email,
                "provincia": provincia,
                "fecha_registro": fecha_registro,
                "segmento": segmento,
            }
        )

    return pd.DataFrame(clientes)


def _generar_pedidos(
    rnd: random.Random,
    config: ConfiguracionDatos,
    clientes: pd.DataFrame,
) -> pd.DataFrame:
    pedidos = []
    pesos_segmento = {
        "alto_valor": 12.0,
        "frecuente": 5.0,
        "ocasional": 1.2,
        "inactivo": 0.12,
    }

    clientes_dict = clientes.to_dict("records")
    for pedido_id in range(1, config.cantidad_pedidos + 1):
        fecha = _fecha_pedido_con_estacionalidad(rnd, config.fecha_inicio_pedidos, config.fecha_fin_pedidos)
        elegibles = [cliente for cliente in clientes_dict if cliente["fecha_registro"] <= fecha]
        cliente = rnd.choices(
            elegibles,
            weights=[pesos_segmento[cliente["segmento"]] for cliente in elegibles],
            k=1,
        )[0]

        estado = rnd.choices(
            ["Completado", "Cancelado", "Pendiente", "En preparacion"],
            weights=[0.86, 0.06, 0.05, 0.03],
            k=1,
        )[0]
        canal_venta = rnd.choices(CANALES, weights=[0.42, 0.24, 0.18, 0.10, 0.06], k=1)[0]

        if rnd.random() < 0.02:
            canal_venta = canal_venta.upper()
        if rnd.random() < 0.015:
            estado = estado.lower()
        if rnd.random() < 0.01:
            estado = f"{estado} "

        pedidos.append(
            {
                "pedido_id": pedido_id,
                "cliente_id": cliente["cliente_id"],
                "fecha": fecha,
                "estado": estado,
                "canal_venta": canal_venta,
            }
        )

    return pd.DataFrame(pedidos)


def _generar_detalle_pedido(
    rnd: random.Random,
    pedidos: pd.DataFrame,
    productos: pd.DataFrame,
) -> pd.DataFrame:
    detalles = []
    productos_dict = productos.to_dict("records")
    pesos_productos = [producto["peso_demanda"] for producto in productos_dict]
    detalle_id = 1

    for pedido in pedidos.to_dict("records"):
        cantidad_items = rnd.choices([1, 2, 3, 4, 5], weights=[0.35, 0.32, 0.20, 0.10, 0.03], k=1)[0]
        productos_pedido = rnd.choices(productos_dict, weights=pesos_productos, k=cantidad_items)

        usados = set()
        for producto in productos_pedido:
            if producto["producto_id"] in usados:
                continue
            usados.add(producto["producto_id"])

            cantidad = rnd.choices([1, 2, 3, 4, 6, 12], weights=[0.58, 0.25, 0.09, 0.05, 0.02, 0.01], k=1)[0]
            if rnd.random() < 0.01:
                cantidad = rnd.choice([18, 24])  # compra mayorista plausible.

            precio_unitario = producto["precio"] * rnd.uniform(0.92, 1.04)
            detalles.append(
                {
                    "detalle_id": detalle_id,
                    "pedido_id": pedido["pedido_id"],
                    "producto_id": producto["producto_id"],
                    "cantidad": cantidad,
                    "precio_unitario": round(precio_unitario, 2),
                }
            )
            detalle_id += 1

    return pd.DataFrame(detalles)


def _generar_pagos(
    rnd: random.Random,
    pedidos: pd.DataFrame,
    detalle_pedido: pd.DataFrame,
) -> pd.DataFrame:
    totales = detalle_pedido.assign(
        total=detalle_pedido["cantidad"] * detalle_pedido["precio_unitario"]
    ).groupby("pedido_id", as_index=False)["total"].sum()
    pedidos_con_total = pedidos.merge(totales, on="pedido_id", how="left")

    pagos = []
    for pago_id, pedido in enumerate(pedidos_con_total.to_dict("records"), start=1):
        estado_pedido = str(pedido["estado"]).strip().lower()
        if estado_pedido == "cancelado":
            estado_pago = rnd.choices(["Rechazado", "Pendiente", "Aprobado"], weights=[0.58, 0.32, 0.10], k=1)[0]
        elif estado_pedido == "pendiente":
            estado_pago = rnd.choices(["Pendiente", "Aprobado", "Rechazado"], weights=[0.70, 0.20, 0.10], k=1)[0]
        else:
            estado_pago = rnd.choices(["Aprobado", "Rechazado", "Pendiente"], weights=[0.91, 0.05, 0.04], k=1)[0]

        monto = round(float(pedido["total"]), 2)
        if estado_pago == "Rechazado":
            monto = 0.0

        fecha_pago = pedido["fecha"] + timedelta(days=rnd.choice([0, 0, 0, 1, 2, 3]))
        metodo_pago = rnd.choices(METODOS_PAGO, weights=[0.36, 0.18, 0.17, 0.22, 0.07], k=1)[0]
        if rnd.random() < 0.015:
            metodo_pago = metodo_pago.lower()

        pagos.append(
            {
                "pago_id": pago_id,
                "pedido_id": pedido["pedido_id"],
                "fecha_pago": fecha_pago,
                "monto": monto,
                "metodo_pago": metodo_pago,
                "estado": estado_pago,
            }
        )

    return pd.DataFrame(pagos)


def _generar_movimientos_stock(
    rnd: random.Random,
    productos: pd.DataFrame,
    detalle_pedido: pd.DataFrame,
    pedidos: pd.DataFrame,
) -> pd.DataFrame:
    pedidos_fechas = pedidos[["pedido_id", "fecha", "estado"]]
    ventas = detalle_pedido.merge(pedidos_fechas, on="pedido_id", how="left")
    ventas = ventas[ventas["estado"].astype(str).str.strip().str.lower() != "cancelado"]

    movimientos = []
    movimiento_id = 1

    for producto in productos.to_dict("records"):
        movimientos.append(
            {
                "movimiento_id": movimiento_id,
                "producto_id": producto["producto_id"],
                "fecha": date(2023, 12, 15),
                "tipo": "Ingreso inicial",
                "cantidad": int(producto["stock"]) + rnd.randint(20, 120),
            }
        )
        movimiento_id += 1

    for venta in ventas.to_dict("records"):
        movimientos.append(
            {
                "movimiento_id": movimiento_id,
                "producto_id": venta["producto_id"],
                "fecha": venta["fecha"],
                "tipo": "Venta",
                "cantidad": -int(venta["cantidad"]),
            }
        )
        movimiento_id += 1

    for producto_id in productos["producto_id"].tolist():
        for _ in range(rnd.randint(2, 5)):
            tipo = rnd.choices(["Ingreso proveedor", "Ajuste inventario"], weights=[0.82, 0.18], k=1)[0]
            cantidad = rnd.randint(12, 90) if tipo == "Ingreso proveedor" else rnd.choice([-3, -2, -1, 1, 2, 3])
            movimientos.append(
                {
                    "movimiento_id": movimiento_id,
                    "producto_id": producto_id,
                    "fecha": _fecha_aleatoria(rnd, date(2024, 1, 1), date(2026, 8, 31)),
                    "tipo": tipo,
                    "cantidad": cantidad,
                }
            )
            movimiento_id += 1

    return pd.DataFrame(movimientos)


def _precio_base_categoria(rnd: random.Random, categoria_id: int) -> float:
    rangos = {
        1: (5500, 22000),
        2: (4800, 16000),
        3: (4500, 13500),
        4: (7500, 28000),
        5: (18000, 95000),
        6: (9000, 32000),
        7: (6500, 26000),
        8: (3500, 12000),
        9: (1800, 6500),
        10: (2500, 42000),
    }
    minimo, maximo = rangos[categoria_id]
    return rnd.uniform(minimo, maximo)


def _provincia_con_variacion(rnd: random.Random) -> str:
    provincia = rnd.choices(
        PROVINCIAS_BASE,
        weights=[0.30, 0.24, 0.12, 0.10, 0.08, 0.04, 0.03, 0.03, 0.03, 0.03],
        k=1,
    )[0]
    if provincia in VARIANTES_PROVINCIA and rnd.random() < 0.35:
        return rnd.choice(VARIANTES_PROVINCIA[provincia])
    return provincia


def _fecha_pedido_con_estacionalidad(rnd: random.Random, inicio: date, fin: date) -> date:
    pesos_mensuales = {
        1: 0.80,
        2: 0.78,
        3: 1.05,
        4: 1.10,
        5: 0.95,
        6: 0.92,
        7: 1.18,
        8: 0.98,
        9: 1.08,
        10: 1.15,
        11: 1.32,
        12: 1.75,
    }
    pesos_dia_semana = {
        0: 0.85,
        1: 0.88,
        2: 0.95,
        3: 1.05,
        4: 1.35,
        5: 1.40,
        6: 0.75,
    }

    dias = (fin - inicio).days
    while True:
        candidata = inicio + timedelta(days=rnd.randint(0, dias))
        peso = pesos_mensuales[candidata.month] * pesos_dia_semana[candidata.weekday()]
        if rnd.random() < min(peso / 2.5, 0.95):
            return candidata


def _fecha_aleatoria(rnd: random.Random, inicio: date, fin: date) -> date:
    return inicio + timedelta(days=rnd.randint(0, (fin - inicio).days))


def _slug(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", ".", texto)
    return texto.strip(".")


if __name__ == "__main__":
    datos = generar_datos()
    guardar_csv(datos)
    for nombre, dataframe in datos.items():
        print(f"{nombre}: {dataframe.shape[0]} filas")
