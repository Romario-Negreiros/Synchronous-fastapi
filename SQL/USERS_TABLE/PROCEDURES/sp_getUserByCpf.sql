DELIMITER //
CREATE PROCEDURE sp_getUserByCpf(IN param_cpf VARCHAR(11))
BEGIN
	SELECT cpf, name, password FROM users WHERE cpf=param_cpf;
END //
DELIMITER ;