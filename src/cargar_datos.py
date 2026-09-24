from __future__ import annotations

from typing import Iterable

import pandas as pd

from conexion import obtener_conexion
from generar_datos import ConfiguracionDatos, generar_datos, guardar_csv


ORDEN_CARGA = [
    "categorias",
    "clientes",
    "productos",
    "pedidos",
    "detalle_pedido",
    "pagos",
    "movimientos_stock",
]

ORDEN_BORRADO = list(reversed(ORDEN_CARGA))

TABLAS_SQL = {
    "categorias": "Categorias",
    "clientes": "Clientes",
    "productos": "Productos",
    "pedidos": "Pedidos",
    "detalle_pedido": "DetallePedido",
    "pagos": "Pagos",
    "movimientos_stock": "MovimientosStock",
}

COLUMNAS_SQL = {
    "categorias": ["categoria_id", "nombre", "descripcion"],
    "clientes": ["cliente_id", "nombre", "email", "provincia", "fecha_registro"],
    "productos": ["producto_id", "nombre", "categoria_id", "marca", "precio", "costo", "stock"],
    "pedidos": ["pedido_id", "cliente_id", "fecha", "estado", "canal_venta"],
    "detalle_pedido": ["detalle_id", "pedido_id", "producto_id", "cantidad", "precio_unitario"],
    "pagos": ["pago_id", "pedido_id", "fecha_pago", "monto", "metodo_pago", "estado"],
    "movimientos_stock": ["movimiento_id", "producto_id", "fecha", "tipo", "cantidad"],
}


def cargar_datos_sql_server(
    datasets: dict[str, pd.DataFrame],
    limpiar_tablas: bool = True,
) -> dict[str, int]:
    """Carga los datos en SQL Server respetando el orden de claves foraneas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.fast_executemany = True

    try:
        if limpiar_tablas:
            _limpiar_tablas(cursor)

        filas_insertadas = {}
        for nombre_dataset in ORDEN_CARGA:
            tabla = TABLAS_SQL[nombre_dataset]
            columnas = COLUMNAS_SQL[nombre_dataset]
            dataframe = datasets[nombre_dataset][columnas].copy()
            _insertar_dataframe(cursor, tabla, columnas, dataframe)
            filas_insertadas[tabla] = len(dataframe)

        conexion.commit()
        return filas_insertadas
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def generar_y_cargar(
    config: ConfiguracionDatos | None = None,
    guardar_archivos_csv: bool = True,
    limpiar_tablas: bool = True,
) -> dict[str, int]:
    datos = generar_datos(config)

    if guardar_archivos_csv:
        guardar_csv(datos)

    return cargar_datos_sql_server(datos, limpiar_tablas=limpiar_tablas)


def _limpiar_tablas(cursor) -> None:
    for nombre_dataset in ORDEN_BORRADO:
        tabla = TABLAS_SQL[nombre_dataset]
        cursor.execute(f"DELETE FROM dbo.{tabla}")


def _insertar_dataframe(cursor, tabla: str, columnas: list[str], dataframe: pd.DataFrame) -> None:
    columnas_sql = ", ".join(columnas)
    parametros = ", ".join("?" for _ in columnas)
    sentencia = f"INSERT INTO dbo.{tabla} ({columnas_sql}) VALUES ({parametros})"
    filas = list(_filas_para_sql(dataframe, columnas))

    if not filas:
        return

    usa_identity = _tabla_tiene_identity(cursor, tabla)
    if usa_identity:
        cursor.execute(f"SET IDENTITY_INSERT dbo.{tabla} ON")

    cursor.executemany(sentencia, filas)

    if usa_identity:
        cursor.execute(f"SET IDENTITY_INSERT dbo.{tabla} OFF")
        columna_id = columnas[0]
        maximo_id = int(dataframe[columna_id].max())
        cursor.execute(f"DBCC CHECKIDENT ('dbo.{tabla}', RESEED, ?)", maximo_id)


def _filas_para_sql(dataframe: pd.DataFrame, columnas: list[str]) -> Iterable[tuple]:
    dataframe = dataframe.where(pd.notnull(dataframe), None)
    for fila in dataframe[columnas].itertuples(index=False, name=None):
        yield tuple(_valor_python(valor) for valor in fila)


def _valor_python(valor):
    if hasattr(valor, "item"):
        return valor.item()
    return valor


def _tabla_tiene_identity(cursor, tabla: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sys.identity_columns
        WHERE object_id = OBJECT_ID(?)
        """,
        f"dbo.{tabla}",
    )
    return cursor.fetchone()[0] > 0


if __name__ == "__main__":
    resultado = generar_y_cargar()
    for tabla, filas in resultado.items():
        print(f"{tabla}: {filas} filas insertadas")
