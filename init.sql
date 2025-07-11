create table Cliente(
	idCliente int primary key,
	nombre varchar(50) not null,
	apellido varchar(50) not null,
	telefono varchar(20) not null,
	email varchar(50)
);

create table Vehiculo(
	idVehiculo int primary key,
	idCliente int not null,
	marca varchar(50) not null,
	modelo varchar(50) not null,
	anio int,
	placa varchar(10) not null,
	
	foreign key (idCliente) references Cliente(idCliente)
);

create table Servicio(
	idServicio int primary key,
	idVehiculo int not null,
	descripcion varchar(250) not null,
	fecharegistro datetime not null,
	estado varchar(50),
	
	foreign key (idVehiculo) references Vehiculo(idVehiculo)
);

create table Mecanico(
	idMecanico int primary key,
	nombre varchar(50) not null,
	apellido varchar(50) not null,
	especialidad varchar(50) not null
);

create table Servicio_Mecanico(
	idServicioMecanico int primary key,
	idServicio int not null,
	idMecanico int not null,
	foreign key (idServicio) references Servicio(idServicio),
	foreign key (idMecanico) references Mecanico(idMecanico)
);

create table Factura(
	idFactura int primary key,
	idServicio int not null,
	fechaFactura datetime not null,
	montoDescripcion varchar(500) not null,
	montoTotal decimal not null,
	foreign key (idServicio) references Servicio(idServicio)
);
