from cargar_datos import generar_y_cargar
from generar_datos import ConfiguracionDatos


def main() -> None:
    config = ConfiguracionDatos(semilla=42)
    resultado = generar_y_cargar(config=config, guardar_archivos_csv=True, limpiar_tablas=True)

    print("Carga finalizada correctamente.")
    for tabla, filas in resultado.items():
        print(f"{tabla}: {filas} filas")


if __name__ == "__main__":
    main()
