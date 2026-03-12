-- Creamos y trabajamos dentro de la base de datos
CREATE DATABASE loda;
USE loda;

-- Empezamos creando las tablas
-- Creamos la tabla camión donde también registraremos la hora y fecha ya que los mismos camiones vienen varias veces al dia
CREATE TABLE camion(
	id_camion INT AUTO_INCREMENT PRIMARY KEY,
    matricula_camion VARCHAR(10) NOT NULL,
    matricula_remolque VARCHAR(10),
    transportista VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL
);


-- Creamos la tabla albaran donde registraremos los datos del albará, el total de bultos y lo relacionaremos con la tabla de camión
CREATE TABLE albaran(
	id_albaran INT AUTO_INCREMENT PRIMARY KEY,
    num_albaran VARCHAR(20) NOT NULL,
    num_bultos VARCHAR(10) NOT NULL,
    id_camion INT NOT NULL,
    FOREIGN KEY (id_camion) REFERENCES camion(id_camion)   
    
);


-- Creamos la tabla material para registrar el material y la cantidad que llega en cada albarán
CREATE TABLE material(
	id_material INT AUTO_INCREMENT PRIMARY KEY,
    ref_material VARCHAR(20) NOT NULL,
    descripcion VARCHAR(100) ,
    cantidad INT NOT NULL,
    id_albaran INT NOT NULL,
    FOREIGN KEY (id_albaran) REFERENCES albaran(id_albaran)   
    
);

    
    
    
