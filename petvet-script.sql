CREATE database petvet;
use petvet;
DROP TABLE USERS;
CREATE TABLE users(
	id int AUTO_INCREMENT NOT NULL,
	email varchar(150) NOT NULL UNIQUE,
    password varchar(150) NOT NULL UNIQUE,
    username varchar(150) NOT NULL,
	name varchar(150) NOT NULL,
	type enum('admin','usuario','cliente') NOT NULL,
	PRIMARY KEY(id)
) ENGINE=MyISAM default char set=latin1;

drop table citas;
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