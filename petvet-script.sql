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
	email varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
	PRIMARY KEY(id, email, nombre_mascota),
	FOREIGN KEY(email) REFERENCES users(email)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE citas(
	email varchar(150) NOT NULL,
	nombre_dueno varchar(150) NOT NULL,
	nombre_mascota varchar(150),
	tipo_mascota varchar(150),
    fecha date NOT NULL,
	hora time NOT NULL,
    atencion enum('veterinaria','boutique') NOT NULL,
	PRIMARY KEY(fecha, hora)
) ENGINE=MyISAM default char set=latin1;

INSERT INTO mascotas (email, nombre_mascota, tipo_mascota)
SELECT email, nombre_mascota, tipo_mascota FROM citas;

ALTER TABLE citas ADD FOREIGN KEY(email) REFERENCES users(email),
ADD FOREIGN KEY(nombre_dueno) REFERENCES users(nombre_dueno),
ADD FOREIGN KEY(nombre_mascota) REFERENCES mascotas(nombre_mascota),
ADD FOREIGN KEY(tipo_mascota) REFERENCES mascotas(tipo_mascota);
