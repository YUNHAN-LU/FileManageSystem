CREATE TABLE file_system (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) CHECK (type IN ('file', 'folder')),
  parent_id INT REFERENCES file_system(id) ON DELETE CASCADE,
  disabled BOOL NOT NULL
  );
  
INSERT INTO file_system (id, name, type, parent_id, disabled) VALUES
(0, 'root', 'folder', null, false),
(1, 'Documents', 'folder', 0, false),
(2, 'Images', 'folder', 0, false);

SELECT setval(pg_get_serial_sequence('file_system', 'id'), MAX(id)) FROM file_system;
