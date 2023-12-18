DELIMITER //
CREATE PROCEDURE sp_setUser(IN param_cpf VARCHAR(11), IN param_name VARCHAR(256), IN param_password VARCHAR(256))
BEGIN
	INSERT INTO Users (cpf, name, password) VALUES (param_cpf, param_name, param_password);
END //
DELIMITER ;