from database.db_config import get_connection

def update_syllabus():
    conn = get_connection()
    cursor = conn.cursor()

    # Tech Subjects (MCA, BCA, B.Tech)
    tech_subjects = [
        ("Java", "Introduction to Java only, OOP Concepts, Exception Handling, Multithreading, Collections Framework, JDBC, Servlets, JSP"),
        ("Python", "Python Basics, Data Structures (Lists, Tuples, Dicts), Functions, Modules, File Handling, NumPy, Pandas, Matplotlib"),
        ("C++", "C++ Basics, Classes & Objects, Inheritance, Polymorphism, Templates, STL, File I/O"),
        ("Web Development", "HTML5, CSS3, JavaScript ES6, DOM Manipulation, Bootstrap, Responsive Design, Basic React"),
        ("SQL", "RDBMS Concepts, SQL Commands (DDL, DML, DQL), Joins, Subqueries, Normalization, PL/SQL Basics"),
        ("AI", "Introduction to AI, Search Algorithms, Knowledge Representation, Machine Learning Basics, Neural Networks, NLP Overview")
    ]

    # Management Subjects (MBA, BBA)
    management_subjects = [
        ("Management Principles", "Introduction to Management, Planning, Organizing, Staffing, Directing, Controlling, Leadership Theories"),
        ("Marketing Management", "Market Research, Consumer Behavior, Product Mix, Pricing Strategies, Promotion, Digital Marketing Basics"),
        ("Financial Accounting", "Accounting Concepts, Journal & Ledger, Trial Balance, Balance Sheet, Profit & Loss, Financial Analysis"),
        ("HR Management", "Recruitment & Selection, Training & Development, Performance Appraisal, Compensation Management, Labor Laws"),
        ("Business Economics", "Demand & Supply, Elasticity, Market Structures (Perfect Competition, Monopoly), National Income, Inflation"),
        ("Organizational Behavior", "Individual Behavior, Motivation, Group Dynamics, Team Building, Conflict Management, Change Management")
    ]
    
    # Generate entries for all semesters (1-6)
    semesters = [1, 2, 3, 4, 5, 6]
    
    final_syllabus_list = []

    # Map courses to their subject types
    tech_courses = ["MCA", "BCA", "B.Tech"]
    mgmt_courses = ["MBA", "BBA"]
    
    # 1. Add Tech Subjects
    for course in tech_courses:
        for sem in semesters:
            for subject, content in tech_subjects:
                final_syllabus_list.append((course, sem, subject, content))

    # 2. Add Management Subjects
    for course in mgmt_courses:
        for sem in semesters:
            for subject, content in management_subjects:
                final_syllabus_list.append((course, sem, subject, content))

    print("Updating Syllabus with differentiated subjects...")
    
    try:
        # We will delete these specific subjects to ensure fresh insert
        # To avoid deleting everything, we will delete based on course + subject name from our lists
        
        for entry in final_syllabus_list:
            course, sem, subject, content = entry
            
            # Delete existing to prevent duplicates
            cursor.execute("DELETE FROM syllabus WHERE course=%s AND semester=%s AND subject=%s", (course, sem, subject))
            
            # Split content into units (naive split by comma)
            parts = [p.strip() for p in content.split(',')]
            # Ensure 5 units
            units = [""] * 5
            for i in range(min(5, len(parts))):
                units[i] = parts[i]
            # If more than 5 parts, append remaining to unit 5
            if len(parts) > 5:
                units[4] += ", " + ", ".join(parts[5:])

            cursor.execute("""
                INSERT INTO syllabus (course, semester, subject, unit1, unit2, unit3, unit4, unit5)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (course, sem, subject, units[0], units[1], units[2], units[3], units[4]))
            # print(f"Inserted: {course} Sem {sem} - {subject}") # Commenting out to reduce spam

        conn.commit()
        print("✅ Syllabus differentiated and updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating syllabus: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_syllabus()
