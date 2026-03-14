import mysql.connector
from database.db_config import get_connection
import random
import datetime

def populate_full_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        print("🚀 Starting comprehensive data population...")

        # 1. Clear Tables
        tables = ["students", "attendance", "timetable", "syllabus", "exam_schedule"]
        for t in tables:
            cur.execute(f"DELETE FROM {t}")
        print("🗑️  Cleared existing data.")

        # 2. Setup Data Sources
        courses = ["MCA", "MBA", "BCA", "BBA", "B.Tech"]
        semesters = [1, 2, 3, 4, 5, 6]
        subjects_pool = {
            "MCA": ["Python", "AI", "Cloud Computing", "Data Mining", "Web Dev"],
            "MBA": ["Management", "Finance", "Marketing", "HR", "Economics"],
            "BCA": ["C++", "Java", "DBMS", "Networking", "Maths"],
            "BBA": ["Business Law", "Accounts", "Communication", "Sales", "Stats"],
            "B.Tech": ["Physics", "Mechanics", "Circuits", "Programming", "ED"]
        }
        
        # 3. Insert Students & Attendance
        student_data = []
        attendance_data = []
        count = 1
        
        for course in courses:
            for i in range(40): # 40 students per course
                roll = count
                name = f"Student {count:03d}"
                password = "123"
                student_data.append((roll, name, course, password))
                
                attended = random.randint(50, 100)
                attendance_data.append((roll, 100, attended))
                count += 1

        cur.executemany("INSERT INTO students (roll_no, name, course, password) VALUES (%s, %s, %s, %s)", student_data)
        cur.executemany("INSERT INTO attendance (roll_no, total_classes, attended_classes) VALUES (%s, %s, %s)", attendance_data)
        print(f"✅ inserted {len(student_data)} students.")

        # 4. Insert Timetables
        timetable_data = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        for course in courses:
            subjects = subjects_pool[course]
            for sem in semesters:
                for day in days:
                    # Randomize periods
                    periods = random.sample(subjects, 5) # 5 periods
                    timetable_data.append((course, sem, day, periods[0], periods[1], periods[2], periods[3], periods[4]))

        cur.executemany("""INSERT INTO timetable (course, semester, day, period1, period2, period3, period4, period5) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", timetable_data)
        print("✅ Inserted timetables.")

        # 5. Insert Syllabus
        syllabus_data = []
        for course in courses:
            for sem in semesters:
                for subject in subjects_pool[course]:
                    units = [f"Introduction to {subject}", f"Advanced {subject}", f"{subject} in Practice", f"Case Studies in {subject}", f"Future of {subject}"]
                    syllabus_data.append((course, sem, subject, units[0], units[1], units[2], units[3], units[4]))
        
        cur.executemany("""INSERT INTO syllabus (course, semester, subject, unit1, unit2, unit3, unit4, unit5) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", syllabus_data)
        print("✅ Inserted syllabus.")

        # 6. Insert Exam Schedule
        exam_data = []
        base_date = datetime.date.today() + datetime.timedelta(days=30)
        
        for course in courses:
            for sem in semesters:
                s_count = 0
                for subject in subjects_pool[course]:
                    exam_date = base_date + datetime.timedelta(days=s_count*2)
                    exam_data.append((course, sem, subject, exam_date))
                    s_count += 1
        
        cur.executemany("INSERT INTO exam_schedule (course, semester, subject, exam_date) VALUES (%s, %s, %s, %s)", exam_data)
        print("✅ Inserted exam schedule.")

        conn.commit()
        conn.close()
        print("🎉 All data populated successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    populate_full_data()
