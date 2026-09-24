import pyodbc

SERVER = "DESKTOP-EEKR1H2"
DATABASE = "DataPracticeLab"
DRIVERS = [
    "ODBC Driver 17 for SQL Server",
    "SQL Server",
]


def obtener_conexion():
    errores = []

    for driver in DRIVERS:
        try:
            return pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={SERVER};"
                f"DATABASE={DATABASE};"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
                "Trusted_Connection=yes;"
            )
        except pyodbc.Error as error:
            errores.append(f"{driver}: {error}")

    detalle = "\n".join(errores)
    raise ConnectionError(f"No se pudo conectar a SQL Server.\n{detalle}")

