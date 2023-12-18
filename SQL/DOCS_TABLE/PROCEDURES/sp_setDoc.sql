DELIMITER //
CREATE PROCEDURE sp_setDoc(IN param_type VARCHAR(256), IN param_owner VARCHAR(11), IN param_emissionDate DATETIME)
BEGIN
	INSERT INTO Docs (type, owner, emissionDate) VALUES (param_type, param_owner, param_emissionDate);
END // 
DELIMITER ;