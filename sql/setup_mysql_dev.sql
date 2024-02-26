-- Create database if it doesn't exists
CREATE DATABASE IF NOT EXISTS rdmp_dev_db;

-- Create a user they do not exist
CREATE USER IF NOT EXISTS 'rdmp_dev'@'localhost' IDENTIFIED BY 'rdmp_dev_pwd';

-- Grant all privileges on rdmp_dev_db to rdmp_dev
GRANT ALL PRIVILEGES ON rdmp_dev_db.* TO 'rdmp_dev'@'localhost';

-- Grant all priviledges to rdmp_dev on database rdmp_dev_to
GRANT SELECT ON performance_schema.* TO  'rdmp_dev'@'localhost';
