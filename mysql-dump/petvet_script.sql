drop database IF EXISTS petvet;
CREATE database petvet;
use petvet;
CREATE TABLE users(
	fecha_creacion DATE NOT NULL,
	id int unsigned AUTO_INCREMENT NOT NULL,
	email varchar(150) NOT NULL UNIQUE,
    password varchar(150) NOT NULL,
    username varchar(150) NOT NULL UNIQUE,
	name varchar(150) NOT NULL,
	type enum('admin','usuario','cliente') NOT NULL,
	PRIMARY KEY(id)
) ENGINE=MyISAM default char set=latin1;

CREATE TRIGGER fecha_insert BEFORE INSERT ON users
    FOR EACH ROW SET NEW.fecha_creacion = NOW();

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
    fecha date NOT NULL,
	hora time NOT NULL,
    atencion enum('veterinaria','boutique') NOT NULL,
	UNIQUE (fecha, hora, atencion),
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE recetas(
	id int unsigned AUTO_INCREMENT NOT NULL,
	fecha TIMESTAMP NOT NULL,
	client_id int unsigned NOT NULL,
	doctor_id int unsigned NOT NULL,
	mascota_id int unsigned NOT NULL,
	aplicacion varchar(500),
	FOREIGN KEY (client_id) REFERENCES users (id),
	FOREIGN KEY (doctor_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
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
	fecha datetime NOT NULL,
	user_id int unsigned NOT NULL,
	mascota_id int unsigned NOT NULL,
	descripcion varchar(500),
	subtotal decimal(10,2) unsigned NOT NULL,
	iva decimal(10,2) unsigned NOT NULL,
	total decimal(10,2) unsigned NOT NULL,
	UNIQUE (fecha, user_id, mascota_id),
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (mascota_id) REFERENCES mascotas (id),
	PRIMARY KEY (id)
) ENGINE=MyISAM default char set=latin1;

CREATE TABLE servicios_atencion (
	atencion_id int unsigned NOT NULL,
	servicio_id int unsigned NOT NULL,
	FOREIGN KEY (atencion_id) REFERENCES atenciones (id),
	FOREIGN KEY (servicio_id) REFERENCES servicios (id)
)ENGINE=MyISAM default char set=latin1;

CREATE TABLE medicinas_atencion (
	atencion_id int unsigned NOT NULL,
	medicinas_id int unsigned NOT NULL,
	FOREIGN KEY (atencion_id) REFERENCES atenciones (id),
	FOREIGN KEY (medicinas_id) REFERENCES medicinas (id)
)ENGINE=MyISAM default char set=latin1;

CREATE TABLE medicinas_receta (
	receta_id int unsigned NOT NULL,
	medicinas_id int unsigned NOT NULL,
	FOREIGN KEY (receta_id) REFERENCES recetas (id),
	FOREIGN KEY (medicinas_id) REFERENCES medicinas (id)
)ENGINE=MyISAM default char set=latin1;

INSERT INTO users (fecha_creacion,email,username,password,name,type) VALUES (CURDATE(),'luis@gmail.com','luis','$5$rounds=535000$656MRtarbYnV5bBM$1kwFoigovLgyRQz/Q/UL0wn61L34fFOhHPkKiZiig62' ,'Luis Hernández', 'admin');
INSERT INTO medicinas (nombre,descripcion, presentacion, medida, stock, precio) VALUES('Acepromazine', 'Tranquilizante/sedante para perros, gatos, caballos y otros animales.',
                      'Pastillas', 'mg', '10', '100');
INSERT INTO medicinas (nombre,descripcion, presentacion, medida, stock, precio) VALUES('Codeine',
                      'Usada para tratar el dolor leve a moderado en mascotas. También se puede usar como un supresor de la tos o como medicamento contra la diarrea.',
                      'Pastillas', 'mg', '5', '250');
INSERT INTO medicinas (nombre,descripcion, presentacion, medida, stock, precio) VALUES('Brosin',
                      'Para el tratamiento de heridas simples o infectadas, llagas, quemaduras, dermatitis pústulas y eccema.',
                      'Pomada', 'mg', '3', '125');  