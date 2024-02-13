-- Create database if it doesn't exists
CREATE DATABASE IF NOT EXISTS rdmp_test_db;

-- Create a user they do not exist
CREATE USER IF NOT EXISTS 'rdmp_test'@'localhost' IDENTIFIED BY 'rdmp_test_pwd';

-- Grant all privileges on rdmp_test_db to rdmp_test
GRANT ALL PRIVILEGES ON rdmp_test_db.* TO 'rdmp_test'@'localhost';

-- Grant all priviledges to rdmp_test on database rdmp_test_to
GRANT SELECT ON performance_schema.* TO  'rdmp_test'@'localhost';
