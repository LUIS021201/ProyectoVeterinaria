CREATE database petvet;
use petvet;
CREATE TABLE users(
	id int AUTO_INCREMENT NOT NULL,
	email varchar(150) NOT NULL UNIQUE,
    password varchar(150) NOT NULL,
    username varchar(150) NOT NULL UNIQUE,
	name varchar(150) NOT NULL,
	type enum('admin','usuario','cliente') NOT NULL,
	PRIMARY KEY(id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE mascotas(
	id int AUTO_INCREMENT NOT NULL,
	user_id int NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
	UNIQUE (user_id, nombre_mascota),
	FOREIGN KEY (user_id) REFERENCES users (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE citas(
	id int AUTO_INCREMENT NOT NULL,
	user_id int NOT NULL,
	mascota_id int NOT NULL,
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
	id int AUTO_INCREMENT NOT NULL,
	user_id int NOT NULL,
	mascota_id int NOT NULL,
    nombre_dueno varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
	fecha date NOT NULL,
	medicamento varchar(150) NOT NULL,
	cantidad int,
	intervalos varchar(200),
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

INSERT INTO mascotas (email, nombre_mascota, tipo_mascota)
SELECT email, nombre_mascota, tipo_mascota FROM citas;

