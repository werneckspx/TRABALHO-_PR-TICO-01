DROP DATABASE IF EXISTS doenca;
CREATE DATABASE IF NOT EXISTS doenca;
USE doenca;

CREATE TABLE patogeno (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(32) NOT NULL,
	tipo VARCHAR(8) NOT NULL
);

CREATE TABLE sintomas (
	id INT PRIMARY KEY AUTO_INCREMENT, 
	nome VARCHAR(64) NOT NULL
);

CREATE TABLE doença (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome_tecnico VARCHAR(32) NOT NULL,
	CID VARCHAR(8) NOT NULL,
	id_patogeno INT,
	CONSTRAINT FOREIGN KEY(id_patogeno) REFERENCES patogeno(id)
);

CREATE TABLE nomes_populares (
	doença_id INT, 
	nome VARCHAR(32),
	CONSTRAINT PRIMARY KEY (doença_id, nome),
	CONSTRAINT FOREIGN KEY(doença_id) REFERENCES doença(id)
);

CREATE TABLE apresenta (
	doença_id INT, 
	sintoma_id INT,
	frequencia VARCHAR(16) NOT NULL,
	CONSTRAINT PRIMARY KEY (doença_id, sintoma_id),
	CONSTRAINT FOREIGN KEY(doença_id) REFERENCES doença(id),
	CONSTRAINT FOREIGN KEY(sintoma_id) REFERENCES sintomas(id)
);



SHOW TABLES;