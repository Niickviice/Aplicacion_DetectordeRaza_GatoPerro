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

/*el password '1234' tiene password_hash='$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO'*/$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('arcade_fire@gmail.com','','Alberto Noruega','56765432','325fde34trfd34','2021-07-31T15:18:28+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('eslaguitarradelolo@gmail.com','$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO','Thom Yorke','55880099','898gt957ttj9j','2021-08-31T15:15:30+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Kid_A@gmail.com','$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO','María Magdalena','52932793','op2k1ou90jew','2021-07-31T15:16:08+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Beach_house@gmail.com','$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO','Mariana Villalon','52243432','13hs8d9wtrfd34','2021-07-31T15:09:22+08:00');
INSERT INTO app.users(email, password_hash, nombre, telefono, ruta_avatar, fecha_registro) VALUES('Men_i_trust@gmail.com','$2b$12$mDzoRKwt4pyIo3EThrsWFeKiUUVrpTPdF2V3YD/OG1AcQxuMGe3QO','Leida Figueroa','55094413','0ds3ed9j90qq0','2021-07-31T15:16:00+08:00');

DROP TABLE IF EXISTS app.razas CASCADE;
CREATE TABLE app.razas(
	id SERIAL PRIMARY KEY,	
	raza VARCHAR(300) UNIQUE, /*este nombre debe de coincidir con el de las clases usadas en etrenamiento*/
	raza_alias VARCHAR(300),
	especie VARCHAR(300),
	descripcion VARCHAR,
	cuidados VARCHAR
);

INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Boxer','perro','Ojos de color café, patas blancas, Cabeza chata, Color cafe, blanco','Comer croquetas, sacarlo a pasear, Mantenerlo en áreas abiertas');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Chihuahua','perro', 'raza pequeña, con orejas largas, patitas cortas','Perro de caracter nervioso y agresivo, delicado en los frios se debe mantener en lugares cerrados');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Persa','gato', 'Gato con características de pelaje espezo, orejas cortas y patas largas','Cepillarlo diario, cortarle sus garras, cecarlo con una toalla especial después de bañarse');
INSERT INTO app.razas(raza, especie, descripcion, cuidados) VALUES('Maine Coon','gato', 'Gato con características parecido a un lince, con orejas paradas y pelaje esponjoso','No necesita una atención demasiado meticulosa, cepillarl con frecuencia, cuidar los ojos y sus orejas');

INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Abyssinian','gato','Abisinio (gato)');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('american_bulldog','perro','Bulldog americano');      
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('american_pit_bull_terrier','perro','American Pitbull Terrier');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('basset_hound','perro','Basset hound');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('beagle','perro','Beagle');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Bengal','gato','Bengal');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Birman','gato','Birmano');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Bombay','gato','Bombay');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('boxer','perro','Boxer');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('British_Shorthair','gato','Británico de pelo corto');      
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('chihuahua','perro','Chihuahua');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Egyptian_Mau','gato','Mau egipcio');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('english_cocker_spaniel','perro','Cocker spaniel inglés');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('english_setter','perro','Setter inglés');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('german_shorthaired','perro','Braco alemán de pelo corto');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('great_pyrenees','perro','Perro de montaña de los pirineos');     
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('havanese','perro','Bichón habanero');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('japanese_chin','perro','Spaniel japonés');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('keeshond','perro','Keeshond');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('leonberger','perro','Leonberger');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Maine_Coon','gato','Maine Coon');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('miniature_pinscher','perro','Pinscher miniatura');   
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('newfoundland','perro','Perro de Terranova');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Persian','gato','Persiana americana');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('pomeranian','perro','Pomerania (perro)');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('pug','perro','Pug');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Ragdoll','gato','Ragdoll');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Russian_Blue','gato','Azul ruso');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('saint_bernard','perro','Saint Bernard');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('samoyed','perro','Samoyedo');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('scottish_terrier','perro','Terrier escocés');        
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('shiba_inu','perro','Shiba Inu');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Siamese','gato','Siamés');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('Sphynx','gato','Esfinge');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('staffordshire_bull_terrier','perro','Staffordshire bull terrier');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('wheaten_terrier','perro','Irish soft coated wheaten terrier');
INSERT INTO app.razas(raza, especie, raza_alias) VALUES('yorkshire_terrier','perro','Yorkshire terrier'); 


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