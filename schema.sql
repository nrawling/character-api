create table characters ( 
	character_id INT AUTO_INCREMENT NOT NULL,
	character_name VARCHAR(255) NOT NULL,
	character_race VARCHAR(255) NOT NULL,
	character_class VARCHAR(255) NOT NULL,
	character_level INT NOT NULL,
	PRIMARY KEY (character_id)
);
