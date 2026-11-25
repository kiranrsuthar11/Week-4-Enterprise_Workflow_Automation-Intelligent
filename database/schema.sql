-- Reference schema for SQLite. The application creates the same tables via SQLAlchemy.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'user',
  is_active BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS departments (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY,
  employee_code VARCHAR(30) NOT NULL UNIQUE,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  job_title VARCHAR(120) NOT NULL DEFAULT '',
  status VARCHAR(30) NOT NULL DEFAULT 'Active',
  department_id INTEGER REFERENCES departments(id),
  created_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY,
  original_name VARCHAR(255) NOT NULL,
  stored_name VARCHAR(255) NOT NULL UNIQUE,
  extension VARCHAR(12) NOT NULL,
  size_bytes INTEGER NOT NULL,
  sha256 VARCHAR(64) NOT NULL UNIQUE,
  category VARCHAR(50) NOT NULL DEFAULT 'General',
  extracted_text TEXT NOT NULL DEFAULT '',
  uploaded_by INTEGER REFERENCES users(id),
  created_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS workflows (
  id INTEGER PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status VARCHAR(30) NOT NULL DEFAULT 'Pending',
  document_id INTEGER REFERENCES documents(id),
  created_by INTEGER REFERENCES users(id),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS workflow_activities (
  id INTEGER PRIMARY KEY,
  workflow_id INTEGER NOT NULL REFERENCES workflows(id),
  actor VARCHAR(80) NOT NULL DEFAULT 'system',
  action VARCHAR(40) NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  created_at DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_employees_name ON employees(name);
CREATE INDEX IF NOT EXISTS ix_documents_sha256 ON documents(sha256);
CREATE INDEX IF NOT EXISTS ix_workflows_status ON workflows(status);
