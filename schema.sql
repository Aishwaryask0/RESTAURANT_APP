CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

CREATE TABLE categories (
    cat_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500)
);

CREATE TABLE food (
    food_id INT PRIMARY KEY AUTO_INCREMENT,
    cat_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description VARCHAR(500),
    FOREIGN KEY (cat_id) REFERENCES categories(cat_id)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (food_id) REFERENCES food(food_id)
);

INSERT INTO categories(name , description) VALUES
('North Indian','Spicy and rich curries from North India'),
('South Indian','Dosas,Idlis and more from SOuth India'),
('Chinese','Indo-Chinese blend popular street foods'),
('Snacks', 'Quick bites and finger foods');

INSERT INTO food(cat_id,name, price,description) VALUES
(1,'Butter Chicken',280,'made with butter and chicken classic'),
(2,'Dosa',60,'fresh dosa with some chutney snd palya'),
(3,'Eggroll',80, NULL),
(4,'French Fries',120,NULL);

INSERT INTO users(name,email,password) VALUES
('Akhil','akhil@gmail.com','akhilsk');

INSERT INTO admin(name,email,password) VALUES
('Aishwarya','aishwarya@gmail.com','aishwaryask');

INSERT INTO orders(user_id,food_id,quantity) VALUES
(1,2,3);

CREATE TABLE bookings(
    bookind_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    data Date,
    time TIME,
    guests INT,
    status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);