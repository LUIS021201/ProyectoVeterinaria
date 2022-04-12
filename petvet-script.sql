CREATE database petvet;
use petvet;
CREATE TABLE users(
	email varchar(150) NOT NULL,
    password varchar(150) NOT NULL,
    username varchar(150) NOT NULL,
	name varchar(150) NOT NULL,
	type enum('admin','usuario','cliente') NOT NULL
) ENGINE=MyISAM default char set=latin1;