from database.db_config import get_connection

def get_attendance(roll_no):
    """Fetches attendance for a given roll number."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT total_classes, attended_classes FROM attendance WHERE roll_no=%s", (roll_no,))
        r = cur.fetchone()
        conn.close()

        if r:
            total, attended = r
            percentage = round((attended / total) * 100, 2)
            return {"status": "success", "data": {"percentage": percentage, "total": total, "attended": attended}}
        else:
            return {"status": "error", "message": "Roll number not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
