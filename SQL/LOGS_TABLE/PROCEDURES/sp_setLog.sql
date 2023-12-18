DELIMITER //
CREATE PROCEDURE sp_setLog(
	IN param_full_log VARCHAR(256),
    IN param_log_level VARCHAR(256),
    IN param_issued_from VARCHAR(256),
    IN param_issued_at DATETIME)
BEGIN
	INSERT INTO Logs (full_log, log_level, issued_from, issued_at) VALUES(param_full_log, param_log_level, param_issued_from, param_issued_at);
END //
DELIMITER ;