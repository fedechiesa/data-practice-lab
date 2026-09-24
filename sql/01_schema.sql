/*
DataPracticeLab - Database Schema

Script de esquema no destructivo para DataPracticeLab.
Crea la base y las tablas solamente si no existen.
No elimina tablas, no borra datos y no modifica informacion existente.
*/

IF DB_ID(N'DataPracticeLab') IS NULL
BEGIN
    CREATE DATABASE [DataPracticeLab];
END;
GO

USE [DataPracticeLab];
GO

IF OBJECT_ID(N'dbo.Categorias', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Categorias (
        categoria_id int IDENTITY(1,1) NOT NULL,
        nombre varchar(100) NOT NULL,
        descripcion varchar(255) NULL,
        CONSTRAINT PK_Categorias PRIMARY KEY (categoria_id),
        CONSTRAINT UQ_Categorias_nombre UNIQUE (nombre)
    );
END;
GO

IF OBJECT_ID(N'dbo.Clientes', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Clientes (
        cliente_id int IDENTITY(1,1) NOT NULL,
        nombre varchar(100) NOT NULL,
        email varchar(150) NOT NULL,
        provincia varchar(100) NULL,
        fecha_registro date NOT NULL,
        CONSTRAINT PK_Clientes PRIMARY KEY (cliente_id),
        CONSTRAINT UQ_Clientes_email UNIQUE (email)
    );
END;
GO

IF OBJECT_ID(N'dbo.Productos', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Productos (
        producto_id int IDENTITY(1,1) NOT NULL,
        nombre varchar(150) NOT NULL,
        categoria_id int NOT NULL,
        marca varchar(100) NULL,
        precio decimal(10,2) NOT NULL,
        costo decimal(10,2) NOT NULL,
        stock int NOT NULL,
        CONSTRAINT PK_Productos PRIMARY KEY (producto_id),
        CONSTRAINT FK_Productos_Categorias
            FOREIGN KEY (categoria_id) REFERENCES dbo.Categorias (categoria_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.Pedidos', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Pedidos (
        pedido_id int IDENTITY(1,1) NOT NULL,
        cliente_id int NOT NULL,
        fecha datetime2(7) NOT NULL,
        estado varchar(50) NOT NULL,
        canal_venta varchar(50) NOT NULL,
        CONSTRAINT PK_Pedidos PRIMARY KEY (pedido_id),
        CONSTRAINT FK_Pedidos_Clientes
            FOREIGN KEY (cliente_id) REFERENCES dbo.Clientes (cliente_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.DetallePedido', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.DetallePedido (
        detalle_id int IDENTITY(1,1) NOT NULL,
        pedido_id int NOT NULL,
        producto_id int NOT NULL,
        cantidad int NOT NULL,
        precio_unitario decimal(10,2) NOT NULL,
        CONSTRAINT PK_DetallePedido PRIMARY KEY (detalle_id),
        CONSTRAINT FK_DetallePedido_Pedidos
            FOREIGN KEY (pedido_id) REFERENCES dbo.Pedidos (pedido_id),
        CONSTRAINT FK_DetallePedido_Productos
            FOREIGN KEY (producto_id) REFERENCES dbo.Productos (producto_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.Pagos', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Pagos (
        pago_id int IDENTITY(1,1) NOT NULL,
        pedido_id int NOT NULL,
        fecha_pago datetime2(7) NOT NULL,
        monto decimal(10,2) NOT NULL,
        metodo_pago varchar(50) NOT NULL,
        estado varchar(50) NOT NULL,
        CONSTRAINT PK_Pagos PRIMARY KEY (pago_id),
        CONSTRAINT FK_Pagos_Pedidos
            FOREIGN KEY (pedido_id) REFERENCES dbo.Pedidos (pedido_id)
    );
END;
GO

IF OBJECT_ID(N'dbo.MovimientosStock', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.MovimientosStock (
        movimiento_id int IDENTITY(1,1) NOT NULL,
        producto_id int NOT NULL,
        fecha datetime2(7) NOT NULL,
        tipo varchar(50) NOT NULL,
        cantidad int NOT NULL,
        CONSTRAINT PK_MovimientosStock PRIMARY KEY (movimiento_id),
        CONSTRAINT FK_MovimientosStock_Productos
            FOREIGN KEY (producto_id) REFERENCES dbo.Productos (producto_id)
    );
END;
GO
