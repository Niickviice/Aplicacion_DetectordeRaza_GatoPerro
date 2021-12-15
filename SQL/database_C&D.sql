DROP TABLE IF EXISTS app.users CASCADE;
CREATE TABLE app.users(
	id SERIAL PRIMARY KEY,
	email VARCHAR(500) UNIQUE,
	password_hash VARCHAR(800),
	nombre VARCHAR(300),
	telefono VARCHAR(100),
	ruta_avatar VARCHAR(5000),
	fecha_registro TIMESTAMP WITH TIME ZONE
);

INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('arcade_fire@gmail.com','1234567','Alberto Noruega','56765432','325fde34trfd34','2021-07-31T15:18:28+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('eslaguitarradelolo@gmail.com','674567','Thom Yorke','55880099','898gt957ttj9j','2021-08-31T15:15:30+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Kid_A@gmail.com','0037212','María Magdalena','52932793','op2k1ou90jew','2021-07-31T15:16:08+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Beach_house@gmail.com','0832083','Mariana Villalon','52243432','13hs8d9wtrfd34','2021-07-31T15:09:22+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Men_i_trust@gmail.com','9384756','Leida Figueroa','55094413','0ds3ed9j90qq0','2021-07-31T15:16:00+08:00');

DROP TABLE IF EXISTS app.raza CASCADE;
CREATE TABLE app.razas(
	id SERIAL PRIMARY KEY,
	raza VARCHAR(300) UNIQUE,
	especie VARCHAR(300),
	descripcion VARCHAR,
	cuidados VARCHAR
);

INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Boxer','perro','Ojos de color café, patas blancas, Cabeza chata, Color cafe, blanco','Comer croquetas, sacarlo a pasear, Mantenerlo en áreas abiertas');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Chihuahua','perro', 'raza pequeña, con orejas largas, patitas cortas','Perro de caracter nervioso y agresivo, delicado en los frios se debe mantener en lugares cerrados');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Persa','gato', 'Gato con características de pelaje espezo, orejas cortas y patas largas','Cepillarlo diario, cortarle sus garras, cecarlo con una toalla especial después de bañarse');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Maine Coon','gato', 'Gato con características parecido a un lince, con orejas paradas y pelaje esponjoso','No necesita una atención demasiado meticulosa, cepillarl con frecuencia, cuidar los ojos y sus orejas');


DROP TABLE IF EXISTS app.fotos;
CREATE TABLE app.fotos(
id SERIAL PRIMARY KEY,
id_users INTEGER,
ruta VARCHAR,
correccion_raza VARCHAR,
clasificacion_id_raza_primaria INTEGER,
clasificacion_id_raza_secundaria INTEGER,
clasificacion_id_raza_terciaria INTEGER,
porcentaje_clasificacion_primaria FLOAT,
porcentaje_clasificacion_secundaria FLOAT,
porcentaje_clasificacion_terciaria FLOAT,
fecha TIMESTAMP WITH TIME ZONE,
FOREIGN KEY(id_users) REFERENCES app.users(id),
FOREIGN KEY(clasificacion_id_raza_primaria) REFERENCES app.razas(id),
FOREIGN KEY(clasificacion_id_raza_secundaria) REFERENCES app.razas(id),
FOREIGN KEY(clasificacion_id_raza_terciaria) REFERENCES app.razas(id)
);


INSERT INTO app.fotos(ruta, correccion_raza, fecha) VALUES('1243245654erewr','Pitbull','2021-07-31T15:16:00+08:00');
INSERT INTO app.fotos(ruta, correccion_raza, fecha) VALUES('45JONIOJOD3E','Ragdoll','2021-09-30T15:19:30+08:00');
INSERT INTO app.fotos(ruta, correccion_raza, fecha) VALUES('343onior3555','Munchkin','2021-03-31T15:10:10+08:00');
INSERT INTO app.fotos(ruta, correccion_raza, fecha) VALUES('989h389h4hd3','Mastin','2021-09-13T15:05:24+08:00' );