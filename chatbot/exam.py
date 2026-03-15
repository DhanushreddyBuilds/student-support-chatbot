from database.db_config import get_connection

def get_exam_schedule(course, sem):
    """Fetches exam schedule."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Fixed column name 'sem' -> 'semester'
        cur.execute("SELECT subject, exam_date FROM exam_schedule WHERE course=%s AND semester=%s", (course, sem))
        rows = cur.fetchall()
        conn.close()

        if rows:
            exams = [{"subject": r[0], "date": str(r[1])} for r in rows]
            return {"status": "success", "data": exams}
        else:
            return {"status": "error", "message": "Exam schedule not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
