import mysql.connector
from database.db_config import get_connection

def inspect_schema():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        
        print("Database Schema:")
        for (table_name,) in tables:
            print(f"\nExample Table: {table_name}")
            cur.execute(f"DESCRIBE {table_name}")
            columns = cur.fetchall()
            for col in columns:
                print(f" - {col[0]} ({col[1]})")
                
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    # Redirect stdout to a file with utf-8 encoding
    with open("schema_utf8.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        inspect_schema()

