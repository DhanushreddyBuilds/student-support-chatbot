from database.db_config import get_connection
import os
import datetime

def export_database_native():
    conn = get_connection()
    cursor = conn.cursor()
    
    output_file = os.path.join("database", "student_support_dump_native.sql")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"-- Student Support Database Dump\n")
        f.write(f"-- Generated on: {datetime.datetime.now()}\n\n")
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        for table in tables:
            print(f"Exporting table: {table}")
            f.write(f"\n-- Table structure for table `{table}`\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            
            # Get Create Table statement
            cursor.execute(f"SHOW CREATE TABLE {table}")
            create_stmt = cursor.fetchone()[1]
            f.write(f"{create_stmt};\n\n")
            
            # Get Data
            f.write(f"-- Dumping data for table `{table}`\n")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            if rows:
                # Get column names to handle types if needed, but simple string conversion usually works for basic dump
                # For safety with strings, we should escape quotes.
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            # Escape single quotes and backslashes
                            val_str = str(val).replace('\\', '\\\\').replace("'", "''")
                            values.append(f"'{val_str}'")
                    
                    val_str = ", ".join(values)
                    f.write(f"INSERT INTO `{table}` VALUES ({val_str});\n")
            
            f.write("\n")
            
    print(f"✅ Database exported successfully to: {os.path.abspath(output_file)}")
    conn.close()

if __name__ == "__main__":
    export_database_native()
