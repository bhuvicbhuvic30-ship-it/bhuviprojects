CREATE DATABASE complaint_portal;

USE complaint_portal;

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    usn VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    department_id INT,

    FOREIGN KEY(department_id)
    REFERENCES departments(department_id)
);

CREATE TABLE lecturers (
    lecturer_id INT AUTO_INCREMENT PRIMARY KEY,
    lecturer_name VARCHAR(100),
    employee_id VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    department_id INT,

    FOREIGN KEY(department_id)
    REFERENCES departments(department_id)
);

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,

    complaint_by VARCHAR(20),

    student_id INT NULL,
    lecturer_id INT NULL,

    department_id INT,

    title VARCHAR(255),

    description TEXT,

    status VARCHAR(50) DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id)
    REFERENCES students(student_id),

    FOREIGN KEY(lecturer_id)
    REFERENCES lecturers(lecturer_id),

    FOREIGN KEY(department_id)
    REFERENCES departments(department_id)
);

INSERT INTO departments(department_name)
VALUES
('Computer Science'),
('Information Science'),
('Electronics'),
('Mechanical');

INSERT INTO admin(admin_name,email,password)
VALUES
('Admin','admin@gmail.com','admin123');
