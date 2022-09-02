
CREATE TABLE [pais] (
  [idpais] int identity(1,1) primary key,
  [nompais] varchar(100)
);

CREATE INDEX [PRIMARY key] ON  [pais] ([idpais]);

CREATE TABLE [level_usuarios] (
  [idlevel] int identity(1,1) primary key,
  [desc_level] varchar(15)
);

CREATE INDEX [PRIMARY key] ON  [level_usuarios] ([idlevel]);

create table [categoria](
 [id_categoria] int identity(1,1) primary key,
 [desc_categoria] varchar(50)
);

create table [marca](
	[id_marca] int identity(1,1) primary key,
	[desc_marca] varchar(50)
);

CREATE TABLE [articulos] (
  [idart] int identity(1,1) primary key,
  [descart] varchar(150),
  [prec_compra] float,
  [prec_venta] float,
  [imagen] image,
  [año_modelo] varchar(20),
  [id_categoria] int,
  [id_marca] int,
  foreign key ([id_categoria]) references [categoria]([id_categoria]),
  foreign key ([id_marca]) references [marca]([id_marca])
);

CREATE INDEX [PRIMARY key] ON  [articulos] ([idart]);

CREATE TABLE [tipo_documento] (
  [idtip_doc] int identity(1,1) primary key,
  [desc_doc] varchar(20)
);

CREATE INDEX [PRIMARY key] ON  [tipo_documento] ([idtip_doc]);

CREATE TABLE [documento] (
  [id_doc] int identity(1,1) primary key,
  [id_tip_doc] int,
  [desc_doc] varchar(20),
  CONSTRAINT [FK_documento.id_tip_doc]
    FOREIGN KEY ([id_tip_doc])
      REFERENCES [tipo_documento]([idtip_doc])
);

CREATE INDEX [PRIMARY key] ON  [documento] ([id_doc]);

CREATE TABLE [region] (
  [idreg] int identity(1,1) primary key,
  [nomreg] varchar(100),
  [idpais] int,
  CONSTRAINT [FK_region.idpais]
    FOREIGN KEY ([idpais])
      REFERENCES [pais]([idpais])
);

CREATE INDEX [PRIMARY key] ON  [region] ([idreg]);

CREATE TABLE [provincia] (
  [idprov] int identity(1,1) primary key,
  [nomprov] varchar(100),
  [idreg] int,
  CONSTRAINT [FK_provincia.idreg]
    FOREIGN KEY ([idreg])
      REFERENCES [region]([idreg])
);

CREATE INDEX [PRIMARY key] ON  [provincia] ([idprov]);

CREATE TABLE [ciudad] (
  [idciudad] int identity(1,1) primary key,
  [nomciudad] varchar(100),
  [idprov] int,
  CONSTRAINT [FK_ciudad.idprov]
    FOREIGN KEY ([idprov])
      REFERENCES [provincia]([idprov])
);

CREATE INDEX [PRIMARY key] ON  [ciudad] ([idciudad]);

CREATE TABLE [sector] (
  [idsector] int identity(1,1) primary key,
  [nomsector] varchar(100),
  [idciudad] int,
  CONSTRAINT [FK_sector.idciudad]
    FOREIGN KEY ([idciudad])
      REFERENCES [ciudad]([idciudad])
);

CREATE INDEX [PRIMARY key] ON  [sector] ([idsector]);

CREATE TABLE [direccion] (
  [iddireccion] int identity(1,1) primary key,
  [nomdireccion] varchar(100),
  [idsector] int,
  CONSTRAINT [FK_direccion.idsector]
    FOREIGN KEY ([idsector])
      REFERENCES [sector]([idsector])
);

CREATE INDEX [PRIMARY key] ON  [direccion] ([iddireccion]);

CREATE TABLE [persona] (
  [idpersona] int identity(1,1) primary key,
  [nom_persona] varchar(50),
  [ape_persona] varchar(50),
  [iddireccion] int,
  [telefono] int,
  [genero] char(1),
  [id_doc] int,
  CONSTRAINT [FK_persona.id_doc]
    FOREIGN KEY ([id_doc])
      REFERENCES [documento]([id_doc]),
  CONSTRAINT [FK_persona.iddireccion]
    FOREIGN KEY ([iddireccion])
      REFERENCES [direccion]([iddireccion])
);

CREATE INDEX [PRIMARY key] ON  [persona] ([idpersona]);

CREATE TABLE [empleados] (
  [idemp] int identity(1,1) primary key,
  [idpersona] int,
  [cargo] varchar(50),
  CONSTRAINT [FK_empleados.idpersona]
    FOREIGN KEY ([idpersona])
      REFERENCES [persona]([idpersona])
);

CREATE INDEX [PRIMARY key] ON  [empleados] ([idemp]);

CREATE TABLE [usuarios] (
  [iduser] int identity(1,1) primary key,
  [user] varchar(15),
  [password] varchar(20),
  [idemp] int,
  [id_level] int,
  CONSTRAINT [FK_usuarios.idemp]
    FOREIGN KEY ([idemp])
      REFERENCES [empleados]([idemp]),
  CONSTRAINT [FK_usuarios.id_level]
    FOREIGN KEY ([id_level])
      REFERENCES [level_usuarios]([idlevel])
);

CREATE INDEX [PRIMARY key] ON  [usuarios] ([iduser]);

CREATE TABLE [compras] (
  [idcompras] int identity(1,1) primary key,
  [fecha_compras] date,
  [id_cli] date,
  [iduser] int,
  [total] float,
  CONSTRAINT [FK_compras.iduser]
    FOREIGN KEY ([iduser])
      REFERENCES [usuarios]([iduser])
);

CREATE INDEX [PRIMARY key] ON  [compras] ([idcompras]);

CREATE TABLE [det_compras] (
  [idcompras] int,
  [idart] int,
  [cantidad] float,
  [prec_compras] float,
  [importe] float,
  CONSTRAINT [FK_det_compras.idart]
    FOREIGN KEY ([idart])
      REFERENCES [articulos]([idart]),
  CONSTRAINT [FK_det_compras.idcompras]
    FOREIGN KEY ([idcompras])
      REFERENCES [compras]([idcompras])
);

CREATE TABLE [status_ventas] (
  [idstatus] int identity(1,1) primary key,
  [desc_status] varchar(15)
);

CREATE INDEX [PRIMARY key] ON  [status_ventas] ([idstatus]);

CREATE TABLE [ventas] (
  [idventas] int identity(1,1) primary key,
  [fecha_ventas] date,
  [id_cli] date,
  [iduser] int,
  [total] float,
  [descuento] float,
  [idstatus] int,
  CONSTRAINT [FK_ventas.iduser]
    FOREIGN KEY ([iduser])
      REFERENCES [usuarios]([iduser]),
  CONSTRAINT [FK_ventas.idstatus]
    FOREIGN KEY ([idstatus])
      REFERENCES [status_ventas]([idstatus])
);

CREATE INDEX [PRIMARY key] ON  [ventas] ([idventas]);

CREATE TABLE [det_ventas] (
  [idventas] int,
  [idart] int,
  [cantidad] float,
  [prec_ventas] float,
  [importe] float,
  CONSTRAINT [FK_det_ventas.idventas]
    FOREIGN KEY ([idventas])
      REFERENCES [ventas]([idventas]),
  CONSTRAINT [FK_det_ventas.idart]
    FOREIGN KEY ([idart])
      REFERENCES [articulos]([idart])
);

CREATE TABLE [almacen] (
  [idalm] int identity(1,1) primary key,
  [nom_alm] varchar(150),
  [id_direccion] int,
  CONSTRAINT [FK_almacen.id_direccion]
    FOREIGN KEY ([id_direccion])
      REFERENCES [direccion]([iddireccion])
);

CREATE INDEX [PRIMARY key] ON  [almacen] ([idalm]);

CREATE TABLE [stock] (
  [idart] int,
  [stock] int,
  [punto_reorden] int,
  [id_alm] int,
  CONSTRAINT [FK_stock.idart]
    FOREIGN KEY ([idart])
      REFERENCES [articulos]([idart]),
  CONSTRAINT [FK_stock.id_alm]
    FOREIGN KEY ([id_alm])
      REFERENCES [almacen]([idalm])
);

CREATE TABLE [proveedor] (
  [idprov] int identity(1,1) primary key,
  [idpersona] int,
  CONSTRAINT [FK_proveedor.idpersona]
    FOREIGN KEY ([idpersona])
      REFERENCES [persona]([idpersona])
);

CREATE INDEX [PRIMARY key] ON  [proveedor] ([idprov]);

CREATE TABLE [temp_det_ventas] (
  [idventas] int,
  [idart] int,
  [cantidad] float,
  [prec_ventas] float,
  [importe] float,
  CONSTRAINT [FK_temp_det_ventas.idventas]
    FOREIGN KEY ([idventas])
      REFERENCES [ventas]([idventas]),
  CONSTRAINT [FK_temp_det_ventas.idart]
    FOREIGN KEY ([idart])
      REFERENCES [articulos]([idart])
);

CREATE TABLE [clientes] (
  [idcli] int identity(1,1) primary key,
  [idpersona] int,
  CONSTRAINT [FK_clientes.idpersona]
    FOREIGN KEY ([idpersona])
      REFERENCES [persona]([idpersona])
);

CREATE INDEX [PRIMARY key] ON  [clientes] ([idcli]);

CREATE TABLE [status] (
  [idstatus] int identity(1,1) primary key,
  [descstatus] varchar(20)
);

CREATE INDEX [PRIMARY key] ON  [status] ([idstatus]);

CREATE TABLE [pedidos_clientes] (
  [idped_cli] int identity(1,1) primary key,
  [idstatus] int,
  [idcli] int,
  CONSTRAINT [FK_pedidos_clientes.idcli]
    FOREIGN KEY ([idcli])
      REFERENCES [empleados]([idemp]),
  CONSTRAINT [FK_pedidos_clientes.idstatus]
    FOREIGN KEY ([idstatus])
      REFERENCES [status]([idstatus])
);

CREATE INDEX [PRIMARY key] ON  [pedidos_clientes] ([idped_cli]);

CREATE TABLE [detalles_pedidos_clientes] (
  [idped_cli] int,
  [idart] int,
  [cant] int,
  [precio_art] float,
  [envio] float,
  [importe] float,
  CONSTRAINT [FK_detalles_pedidos_clientes.idart]
    FOREIGN KEY ([idart])
      REFERENCES [articulos]([idart]),
  CONSTRAINT [FK_detalles_pedidos_clientes.idped_cli]
    FOREIGN KEY ([idped_cli])
      REFERENCES [pedidos_clientes]([idped_cli])
);

