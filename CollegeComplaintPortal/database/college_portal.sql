CREATE DATABASE college_portal;

USE college_portal;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE complaints (
    cid INT AUTO_INCREMENT PRIMARY KEY,
    student_email VARCHAR(100),
    category VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending'
);
