CREATE TABLE IF NOT EXISTS attendance (
    roll_no INT PRIMARY KEY,
    total_classes INT,
    attended_classes INT
);

CREATE TABLE IF NOT EXISTS timetable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course VARCHAR(50),
    sem INT,
    day VARCHAR(20),
    subjects TEXT
);

CREATE TABLE IF NOT EXISTS syllabus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course VARCHAR(50),
    sem INT,
    subject VARCHAR(100),
    unit1 TEXT,
    unit2 TEXT,
    unit3 TEXT,
    unit4 TEXT,
    unit5 TEXT
);

CREATE TABLE IF NOT EXISTS exam_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course VARCHAR(50),
    sem INT,
    subject VARCHAR(100),
    exam_date DATE
);

CREATE TABLE IF NOT EXISTS conversation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT,
    intent VARCHAR(50),
    confidence FLOAT,
    timestamp DATETIME
);
