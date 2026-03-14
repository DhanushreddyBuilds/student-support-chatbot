import mysql.connector
from database.db_config import get_connection
import random

def populate_data():
    try:
        conn = get_connection()
        cur = conn.cursor()

        print("🚀 Starting database population...")

        # Clear existing data (optional, but good for clean state if requested 'update')
        # Check if tables exist first to avoid errors if run partially
        cur.execute("DELETE FROM attendance")
        cur.execute("DELETE FROM students")
        print("🗑️  Cleared existing data.")

        total_classes = 100
        
        students_data = []
        attendance_data = []

        for i in range(1, 201):
            # Roll number as integer. Input "036" becomes 36.
            # If user strictly needs VARCHAR "036" storage, we'd need schema change.
            # Assuming INT is sufficient as int("036") works.
            roll = i 
            name = f"Student {i:03d}" # e.g., "Student 036"
            course = "MCA" if i % 2 == 0 else "MBA"
            password = "123" 
            
            students_data.append((roll, name, course, password))

            attended = random.randint(60, 100)
            attendance_data.append((roll, total_classes, attended))

        # Bulk Insert Students
        sql_student = "INSERT INTO students (roll_no, name, course, password) VALUES (%s, %s, %s, %s)"
        cur.executemany(sql_student, students_data)
        
        # Bulk Insert Attendance
        sql_attendance = "INSERT INTO attendance (roll_no, total_classes, attended_classes) VALUES (%s, %s, %s)"
        cur.executemany(sql_attendance, attendance_data)

        conn.commit()
        conn.close()
        print(f"✅ Successfully added {len(students_data)} students (Roll 001-200) and attendance records.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    populate_data()
