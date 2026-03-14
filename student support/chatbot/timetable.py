from database.db_config import get_connection

def get_timetable(course, sem):
    """Fetches timetable for a given course and semester."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Updated query to match actual schema: 'semester' instead of 'sem'
        cur.execute("""SELECT day, period1, period2, period3, period4, period5 
                       FROM timetable 
                       WHERE course=%s AND semester=%s""", (course, sem))
        rows = cur.fetchall()
        conn.close()

        if rows:
            timetable = []
            for r in rows:
                day = r[0]
                # Filter out empty periods
                periods = [p for p in r[1:] if p]
                timetable.append({"day": day, "subjects": ", ".join(periods)})
            
            return {"status": "success", "data": timetable}
        else:
            return {"status": "error", "message": "Timetable not found for this course/sem."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

