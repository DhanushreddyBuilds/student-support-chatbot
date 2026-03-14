import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_config import get_connection

def verify_system_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("=== STUDENT SUPPORT SYSTEM DIAGNOSTIC ===")
    
    # 1. Check User/Attendance
    cursor.execute("SELECT count(*) FROM attendance")
    user_count = cursor.fetchone()[0]
    print(f"✅ Application Users/Attendance Records: {user_count}")
    
    # 2. Check Timetable Coverage
    print("\n--- Timetable Coverage ---")
    cursor.execute("SELECT course, semester, count(*) FROM timetable GROUP BY course, semester")
    tt_data = cursor.fetchall()
    if tt_data:
        for row in tt_data:
            print(f"  - {row[0]} Sem {row[1]}: {row[2]} entries")
    else:
        print("  ❌ No Timetable data found!")

    # 3. Check Syllabus Coverage
    print("\n--- Syllabus Coverage ---")
    cursor.execute("SELECT course, semester, count(*) FROM syllabus GROUP BY course, semester")
    syl_data = cursor.fetchall()
    if syl_data:
        for row in syl_data:
            print(f"  - {row[0]} Sem {row[1]}: {row[2]} subjects")
    else:
        print("  ❌ No Syllabus data found!")

    # 4. Check Exam Schedule Coverage
    print("\n--- Exam Schedule Coverage ---")
    cursor.execute("SELECT course, semester, count(*) FROM exam_schedule GROUP BY course, semester")
    exam_data = cursor.fetchall()
    if exam_data:
        for row in exam_data:
            print(f"  - {row[0]} Sem {row[1]}: {row[2]} exams")
    else:
        print("  ❌ No Exam Schedule data found!")

    conn.close()
    print("\n=== DIAGNOSTIC COMPLETE ===")

if __name__ == "__main__":
    verify_system_data()
