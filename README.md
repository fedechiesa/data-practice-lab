# Data Practice Lab

Proyecto personal orientado a la práctica de **SQL, Python y análisis de datos** mediante un escenario simulado de ventas minoristas.

El proyecto utiliza una base de datos relacional en **SQL Server** con información sobre clientes, productos, pedidos, pagos y movimientos de stock. A partir de estos datos se desarrollan consultas SQL, procesos de análisis con Python y Pandas, y ejercicios de exploración de datos.

## Objetivo

El objetivo de Data Practice Lab es construir un entorno de práctica que permita trabajar progresivamente sobre un flujo de datos similar al que podría encontrarse en un proyecto real.

A lo largo del proyecto se busca practicar:

- Diseño y consulta de bases de datos relacionales.
- SQL aplicado al análisis de datos.
- Conexión entre Python y SQL Server.
- Manipulación y análisis de datos con Pandas.
- Validación y exploración de datos.
- Desarrollo de análisis orientados a preguntas de negocio.
- Buenas prácticas de organización, documentación y control de versiones con Git.

## Tecnologías

- **Python** — procesamiento, validación y análisis de datos.
- **Pandas** — manipulación y análisis de datasets.
- **SQL Server** — base de datos relacional del proyecto.
- **SQL** — consultas, agregaciones y análisis sobre los datos almacenados.
- **pyodbc** — conexión entre Python y SQL Server.
- **Git / GitHub** — control de versiones y documentación del proyecto.

## Estructura del proyecto

```text
data-practice-lab/
│
├── data/
│   ├── raw/        # Archivos CSV generados y utilizados para la carga inicial
│   └── processed/  # Carpeta reservada para datos procesados
├── database/
│   └── modelo.txt  # Descripción textual del modelo de datos
├── sql/
│   └── 01_schema.sql  # Esquema no destructivo de la base de datos
├── src/
│   ├── conexion.py       # Configuración y conexión a SQL Server
│   ├── generar_datos.py  # Generación de datos sintéticos y CSV
│   ├── cargar_datos.py   # Carga de datos en SQL Server
│   └── main.py           # Punto de entrada para generar y cargar datos
├── .gitignore
└── README.md
```

La estructura busca separar las distintas responsabilidades del proyecto: almacenamiento de datos, definición de la base de datos, procesamiento con Python y análisis exploratorio.

## Modelo de datos

La base de datos representa un sistema simplificado de ventas minoristas. El modelo permite relacionar clientes, productos, pedidos, pagos y movimientos de inventario.

Las principales entidades son:

- **Categorias** — clasificación de los productos disponibles.
- **Productos** — catálogo de productos, incluyendo información comercial y su categoría.
- **Clientes** — información de los clientes registrados.
- **Pedidos** — operaciones de compra realizadas por los clientes.
- **DetallePedido** — productos y cantidades incluidos en cada pedido.
- **Pagos** — información relacionada con el pago de cada pedido.
- **MovimientosStock** — registro de entradas y salidas de inventario.

Las relaciones entre estas entidades permiten analizar el negocio desde distintas perspectivas, como ventas, clientes, productos, categorías, pagos y evolución del stock.

De forma simplificada, el flujo principal de información es:

```text id="zwmd2u"
Categorias
    │
    └── Productos
            │
            └── DetallePedido
                    │
Clientes ─────── Pedidos
                    │
                    └── Pagos

Productos ───── MovimientosStock
```

## Estado actual

Actualmente el proyecto cuenta con una primera versión funcional de la base de datos, generación de datos sintéticos, archivos CSV y carga de datos desde Python hacia SQL Server.

### Base de datos

- Esquema relacional implementado en SQL Server.
- Script para crear la base de datos y sus tablas.
- Versión no destructiva del esquema para evitar eliminar información existente.
- Relaciones mediante claves primarias y foráneas.
- Restricciones de integridad y unicidad.

### Datos

Se generó un conjunto de datos sintéticos para disponer de un volumen suficiente sobre el cual realizar consultas y análisis.

Actualmente la base contiene aproximadamente:

| Entidad | Registros |
|---|---:|
| Categorías | 10 |
| Clientes | 1.000 |
| Productos | 100 |
| Pedidos | 8.000 |
| Detalles de pedido | 16.801 |
| Pagos | 8.000 |
| Movimientos de stock | 16.319 |

También se realizaron validaciones iniciales de calidad e integridad de los datos, incluyendo:

- Verificación de emails duplicados.
- Verificación de claves foráneas huérfanas.
- Control de cantidad de registros generados.

### Python + SQL Server

La conexión entre Python y SQL Server se encuentra implementada mediante `pyodbc`, permitiendo generar datos, guardarlos como CSV y cargarlos en la base de datos.

Esto establece la base para desarrollar las siguientes etapas del proyecto: consultas SQL analíticas, análisis exploratorio y procesamiento de datos con Python.

## Cómo ejecutar el proyecto

### Requisitos

Para trabajar con el proyecto se necesita:

- Python 3
- SQL Server
- SQL Server Management Studio (SSMS) o una herramienta equivalente
- ODBC Driver 17 for SQL Server
- Git

### 1. Clonar el repositorio

```bash id="c2kl6x"
git clone <URL_DEL_REPOSITORIO>
cd data-practice-lab
```

### 2. Crear la base de datos

Ejecutar desde SQL Server Management Studio el script de creación del esquema ubicado en `sql/01_schema.sql`.

El proyecto incluye una versión no destructiva del esquema, que crea la base de datos y las tablas únicamente cuando no existen.

### 3. Cargar los datos

Ejecutar el punto de entrada principal desde Python:

```bash
python src/main.py
```

Este script genera los datos sintéticos, guarda los archivos CSV en `data/raw/` y carga las tablas en SQL Server.

Antes de hacerlo, verificar que la configuración de conexión en `src/conexion.py` corresponda al entorno local.

### 4. Verificar la conexión desde Python

Una vez creada y poblada la base de datos, los scripts del proyecto pueden conectarse a SQL Server mediante `pyodbc` para consultar y cargar los datos.

> Las configuraciones específicas de cada entorno, como el nombre del servidor local, deben revisarse antes de ejecutar el proyecto.

## Próximos pasos

El proyecto continuará desarrollándose progresivamente. Las siguientes etapas previstas son:

- Crear una colección de consultas SQL orientadas a preguntas de negocio.
- Practicar `JOIN`, agregaciones, subconsultas, CTE y funciones de ventana.
- Integrar consultas SQL con Python y Pandas.
- Desarrollar un análisis exploratorio de datos (EDA).
- Incorporar visualizaciones para comunicar los principales resultados.
- Analizar posibles aplicaciones de modelos de Machine Learning sobre los datos generados.

## Sobre el proyecto

Data Practice Lab es un proyecto personal de aprendizaje y práctica continua.

El objetivo no es únicamente obtener resultados, sino construir progresivamente un flujo de trabajo de datos completo, comprender las decisiones tomadas y aplicar buenas prácticas de desarrollo, análisis y documentación.
