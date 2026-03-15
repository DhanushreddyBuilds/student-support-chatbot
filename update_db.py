import mysql.connector
from database.db_config import get_connection

def update_database():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # 1. Ensure 'students' table exists and has password column
        print("Checking 'students' table...")
        cur.execute("SHOW TABLES LIKE 'students'")
        if not cur.fetchone():
            print("Creating 'students' table...")
            cur.execute("""
                CREATE TABLE students (
                    roll_no INT PRIMARY KEY,
                    name VARCHAR(100),
                    course VARCHAR(50),
                    password VARCHAR(255)
                )
            """)
        else:
            print("'students' table exists. Checking for 'password' column...")
            cur.execute("SHOW COLUMNS FROM students LIKE 'password'")
            if not cur.fetchone():
                print("Adding 'password' column...")
                cur.execute("ALTER TABLE students ADD COLUMN password VARCHAR(255)")
            else:
                print("'password' column already exists.")

        # 2. Insert dummy user for testing if empty
        cur.execute("SELECT * FROM students WHERE roll_no=101")
        if not cur.fetchone():
            print("Inserting dummy student (Roll: 101, Pass: 1234)...")
            # In production, passwords should be hashed! keeping simple for now as requested.
            cur.execute("INSERT INTO students (roll_no, name, course, password) VALUES (101, 'John Doe', 'MCA', '1234')")
            conn.commit()

        print("✅ Database update completed successfully.")
        conn.close()

    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    update_database()
