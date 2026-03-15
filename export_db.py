import os
import subprocess
from database.db_config import db_config

def export_database():
    # Configuration
    db_user = db_config['user']
    db_password = db_config['password']
    db_name = db_config['database']
    db_host = db_config['host']
    
    output_file = os.path.join("database", "student_support_dump.sql")
    
    # Check if mysqldump is available (usually in PATH if XAMPP/MySQL added)
    # If not, user might need to point to it, but we'll try default
    
    cmd = f"mysqldump -u {db_user} -p{db_password} -h {db_host} --result-file=\"{output_file}\" {db_name}"
    
    print(f"Exporting database to {output_file}...")
    try:
        # subprocess.run requires shell=True for this command structure on Windows to handle redirects if not using --result-file
        # but --result-file is safer.
        # Note: 'mysqldump' must be in system PATH.
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Database exported successfully to: {os.path.abspath(output_file)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error exporting database: {e}")
        print("Note: Ensure 'mysqldump' is in your system PATH.")

if __name__ == "__main__":
    export_database()
