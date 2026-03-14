# Student Support Chatbot

An AI-powered chatbot for student support, handling queries about attendance, timetable, syllabus, and exam schedules.

## Features
- **Multilingual Support**: English, Kannada, Hindi, Tamil, Telugu.
- **Academic Info**: Attendance, Timetable, Syllabus, Exams.
- **Emotion Detection**: Responds to user emotions (stress, sadness, etc.).
- **Dynamic UI**: Modern, animated chat interface.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Database Setup**:
    - Ensure MySQL is running.
    - Create a database named `student_support`.
    - Run the `database/schema.sql` script to create tables.
    - Update `database/db_config.py` with your credentials.

3.  **Run Application**:
    ```bash
    python app.py
    ```

4.  **Access**:
    Open `http://127.0.0.1:5000` in your browser.
