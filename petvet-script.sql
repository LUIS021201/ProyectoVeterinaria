CREATE database petvet;
use petvet;
CREATE TABLE users(
	id int unsigned AUTO_INCREMENT NOT NULL,
	email varchar(150) NOT NULL UNIQUE,
    password varchar(150) NOT NULL,
    username varchar(150) NOT NULL UNIQUE,
	name varchar(150) NOT NULL,
	type enum('admin','usuario','cliente') NOT NULL,
	PRIMARY KEY(id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE mascotas(
	id int unsigned AUTO_INCREMENT NOT NULL,
	user_id int unsigned NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
	UNIQUE (user_id, nombre_mascota),
	FOREIGN KEY (user_id) REFERENCES users (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE citas(
	id int unsigned AUTO_INCREMENT NOT NULL,
	user_id int unsigned NOT NULL,
	mascota_id int unsigned NOT NULL,
	nombre_dueno varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
    fecha date NOT NULL,
	hora time NOT NULL,
    atencion enum('veterinaria','boutique') NOT NULL,
	UNIQUE (fecha, hora),
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE recetas(
	id int unsigned AUTO_INCREMENT NOT NULL,
	fecha date NOT NULL,
	user_id int unsigned NOT NULL,
	mascota_id int unsigned NOT NULL,
    nombre_dueno varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
	medicamento_id int unsigned NOT NULL,
	medicamento varchar(150) NOT NULL,
	cantidad int unsigned,
	intervalos varchar(200),
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	FOREIGN KEY (medicamento_id) REFERENCES medicinas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE medicinas(
    id int unsigned AUTO_INCREMENT NOT NULL,
	nombre varchar(150) NOT NULL,
    descripcion varchar(300),
	stock int unsigned not null,
    presentacion ENUM('Pomada','Pastillas','Jarabe','Inyectable','Gotas'),
    medida ENUM('mg','ml'),
	precio decimal(10,2) unsigned NOT NULL,
    PRIMARY KEY (id)

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE servicios(
    id int unsigned AUTO_INCREMENT NOT NULL,
	nombre varchar(150) NOT NULL,
    precio decimal(10,2) NOT NULL,
	habilitado boolean not null,
    PRIMARY KEY (id)

)ENGINE=MyISAM default char set=latin1;

CREATE TABLE atenciones(
	id int unsigned AUTO_INCREMENT NOT NULL,
	fecha date NOT NULL,
	user_id int unsigned NOT NULL,
	mascota_id int unsigned NOT NULL,
    nombre_dueno varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	descripcion varchar(500),
	subtotal decimal(10,2) unsigned NOT NULL,
	iva decimal(10,2) unsigned NOT NULL,
	total decimal(10,2) unsigned NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	FOREIGN KEY (medicamento_id) REFERENCES medicinas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

