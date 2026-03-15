from database.db_config import get_connection

def get_syllabus(course, sem, subject):
    """Fetches syllabus for a specific subject."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Fixed column name 'sem' -> 'semester'
        cur.execute("""SELECT unit1, unit2, unit3, unit4, unit5
                       FROM syllabus
                       WHERE course=%s AND semester=%s AND subject=%s""",
                    (course, sem, subject))
        r = cur.fetchone()
        conn.close()

        if r:
            units = [f"Unit {i+1}: {u}" for i, u in enumerate(r)]
            return {"status": "success", "data": units}
        else:
            return {"status": "error", "message": "Syllabus not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
