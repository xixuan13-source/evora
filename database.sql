CREATE DATABASE evora;
USE evora;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

INSERT INTO categories (category_name)
VALUES
('Food'),
('Transport'),
('Shopping'),
('Entertainment'),
('Education'),
('Healthcare'),
('Bills'),
('Others');


CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    category_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    description VARCHAR(255),

    expense_date DATE NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);


CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    category_id INT NOT NULL,

    budget_amount DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    feedback_type VARCHAR(50) NOT NULL,

    comment TEXT NOT NULL,

    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);


-- DEMO DATA
INSERT INTO users
(username, email, password_hash)
VALUES
('Demo User',
 'demo@evora.com',
 'password123');

INSERT INTO expenses
(user_id, category_id, amount, description, expense_date)
VALUES

(1,1,12.50,'Chicken Rice','2025-06-01'),

(1,2,2.10,'MRT','2025-06-01'),

(1,3,45.00,'Uniqlo','2025-06-05'),

(1,1,8.50,'McDonalds','2025-06-06'),

(1,4,15.00,'Movie Ticket','2025-06-10');

INSERT INTO budgets
(user_id, category_id, budget_amount)
VALUES

(1,1,300.00),

(1,2,100.00),

(1,3,150.00);

INSERT INTO feedback
(user_id, feedback_type, comment)
VALUES

(1,'Feature Request', 'Would like recurring expenses feature'),

(1,'Suggestion', 'Dashboard looks good');
