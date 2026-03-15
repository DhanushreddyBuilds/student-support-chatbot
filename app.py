from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database.db_config import get_connection
import datetime
import random
from chatbot.nlp import predict_intent
from chatbot.attendance import get_attendance
from chatbot.timetable import get_timetable
from chatbot.syllabus import get_syllabus
from chatbot.exam import get_exam_schedule
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = "super_secret_key_for_student_ai" # Change this in production

# =========================
# Context Memory & Config
# =========================
user_context = {}

LANGUAGE_MAP = {
    "en": "en",
    "hi": "hi",
    "kn": "kn",
    "ta": "ta",
    "te": "te",
    "ml": "ml",
    "mr": "mr",
    "bn": "bn",
    "gu": "gu",
    "pa": "pa",
    "ur": "ur"
}

# =========================
# Emotion & Helpers
# =========================
EMOTIONS = {
    "stress": ["stress", "pressure", "anxiety", "worried", "tension"],
    "sad": ["sad", "unhappy", "depressed", "low"],
    "fear": ["fear", "scared", "fail", "afraid", "panic"],
    "confused": ["confused", "unsure", "lost", "doubt"],
    "motivated": ["motivated", "excited", "happy", "great"]
}
# ... (rest of emotion responses) ...

def translate_text(text, target_lang):
    """Translates text to target language. Returns original if error or same lang."""
    if target_lang == "en" or not text:
        return text
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

# ... (rest of auth routes) ...


EMOTION_RESPONSES = {
    "stress": "😔 Stay calm — take a deep breath. We’ll figure this out together.",
    "sad": "💙 I'm here for you. You’re not alone.",
    "fear": "🫂 It's okay to be scared. Taking it one step at a time helps.",
    "confused": "🤔 Let's break it down. I'll explain it clearly.",
    "motivated": "🔥 That's the spirit! Keep going!"
}

# =========================
# Auth Routes
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        roll_no = request.form.get("roll_no")
        name = request.form.get("name")
        course = request.form.get("course")
        password = request.form.get("password")

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO students (roll_no, name, course, password) VALUES (%s, %s, %s, %s)",
                        (roll_no, name, course, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("register.html", error="User already exists or error occurred.")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        roll_no = request.form.get("roll_no")
        password = request.form.get("password")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE roll_no=%s AND password=%s", (roll_no, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = roll_no
            session["name"] = user[1] # Assuming Name is 2nd column
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# =========================
# Routes
# =========================
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"reply": "Session expired. Please login again."}), 401

    data = request.json
    raw_message = data.get("message", "").strip()
    target_lang = data.get("language", "en") # Default to English
    uid = request.remote_addr 
    
    if not raw_message:
        return jsonify({"reply": "Please say something!"})

    # 1. Translate Input to English (if not English)
    user_message = raw_message
    if target_lang != "en":
        try:
            print(f"DEBUG: Translating input '{raw_message}' from {target_lang} -> en")
            # Re-instantiate to avoid session issues
            translator = GoogleTranslator(source='auto', target='en')
            user_message = translator.translate(raw_message)
            print(f"DEBUG: Translated input: {user_message}")
        except Exception as e:
            print(f"ERROR: Input Translation Failed: {e}")
            user_message = raw_message # Fallback


    # Context Management
    if uid not in user_context:
        user_context[uid] = {}
    ctx = user_context[uid]

    # Emotion Detection (on English text)
    emotion = detect_emotion(user_message)
    emotion_reply = EMOTION_RESPONSES.get(emotion, "")
    
    # NLP Intent Prediction (on English text)
    intent, confidence = predict_intent(user_message)
    log_conversation(user_message, intent, confidence)

    reply_text = ""
    structured_data = None
    data_type = None

    # -----------------------------
    # LOGIC (Processed in English)
    # -----------------------------
    
    # ... (Keep existing logic, but assign to `reply_text` instead of returning immediately) ...
    # Refactoring slightly to capture reply for translation

    # -----------------------------
    # LOGIC (Processed in English)
    # -----------------------------
    
    # 1. Timetable Context Flow
    if ctx.get("awaiting") == "tt_course":
        ctx["course"] = user_message.upper()
        ctx["awaiting"] = "tt_sem"
        reply_text = "Which semester? (e.g., 1, 2, 3)"
    
    elif ctx.get("awaiting") == "tt_sem":
        if user_message.isdigit():
            ctx["awaiting"] = None
            sem = int(user_message)
            result = get_timetable(ctx["course"], sem)
            if result["status"] == "success":
                reply_text = "Here is the timetable:"
                structured_data = result["data"]
                data_type = "table"
            else:
                reply_text = result["message"]
        else:
            reply_text = "Please enter a valid semester number."

    # 2. Syllabus Context Flow
    elif ctx.get("awaiting") == "syl_course":
        ctx["course"] = user_message.upper()
        ctx["awaiting"] = "syl_sem"
        reply_text = "Which semester?"

    elif ctx.get("awaiting") == "syl_sem":
        if user_message.isdigit():
            ctx["sem"] = int(user_message)
            ctx["awaiting"] = "syl_sub"
            
            # Context-aware suggestions
            course = ctx.get("course", "").upper()
            if course in ["MBA", "BBA"]:
                examples = "(e.g., Marketing, HR, Management)"
            else:
                examples = "(e.g., Python, Java, SQL)"
            
            reply_text = f"Which subject? {examples}"
        else:
            reply_text = "Please enter a valid semester number."

    elif ctx.get("awaiting") == "syl_sub":
        ctx["awaiting"] = None
        subject = user_message
        result = get_syllabus(ctx["course"], ctx["sem"], subject)
        if result["status"] == "success":
             header = [
                 f"📚 Here is the syllabus for {subject}:",
                 f"Found it! Syllabus for {subject} (Sem {ctx['sem']}):"
             ]
             reply_text = random.choice(header)
             structured_data = result["data"]
             data_type = "list"
        else:
             reply_text = f"⚠️ {result['message']}"

    # 3. Exam Context Flow
    elif ctx.get("awaiting") == "exam_course":
        ctx["course"] = user_message.upper()
        ctx["awaiting"] = "exam_sem"
        reply_text = "Which semester?"

    elif ctx.get("awaiting") == "exam_sem":
        if user_message.isdigit():
            ctx["awaiting"] = None
            sem = int(user_message)
            result = get_exam_schedule(ctx["course"], sem)
            if result["status"] == "success":
                 header = [
                     f"📝 Exam Schedule for {ctx['course']} Sem {sem}:",
                     f"Get ready! Here are the exams for {ctx['course']} Sem {sem}:"
                 ]
                 reply_text = random.choice(header)
                 structured_data = result["data"]
                 data_type = "table"
            else:
                reply_text = f"⚠️ {result['message']}"
        else:
            reply_text = "Please enter a valid semester number."


    # Intent-Based Routing (Triggers the flows)
    elif "attendance" in user_message.lower() or intent == "attendance":
        if "user" in session:
            roll_no = int(session["user"])
            result = get_attendance(roll_no)
            if result["status"] == "success":
                d = result["data"]
                responses = [
                    f"Here is your attendance report:\n📊 **{d['percentage']}%**\n(Attended: {d['attended']} / {d['total']} classes)",
                    f"You have attended {d['attended']} out of {d['total']} classes. That's {d['percentage']}%!",
                    f"Attendance Update Your current attendance stands at {d['percentage']}%."
                ]
                reply_text = random.choice(responses)
            else:
                reply_text = f"⚠️ {result['message']}"
        else:
             reply_text = "Please login to view your attendance."

    elif "timetable" in user_message.lower() or intent == "timetable":
        ctx["awaiting"] = "tt_course"
        responses = [
            "I can show you the timetable. Which course are you in? (e.g., MCA, MBA)",
            "Timetable lookup coming up! First, tell me your course name.",
        ]
        reply_text = random.choice(responses)

    elif "syllabus" in user_message.lower() or intent == "syllabus":
        ctx["awaiting"] = "syl_course"
        reply_text = "Sure! Which course? (e.g., MCA, MBA)"
        
    elif "exam" in user_message.lower() or intent == "exam":
        ctx["awaiting"] = "exam_course"
        reply_text = "I can check the exam schedule. Which course?"

    # Direct Syllabus Command
    elif user_message.lower().startswith("syllabus"):
        parts = user_message.split()
        if len(parts) >= 4:
            course, sem, subject = parts[1], parts[2], " ".join(parts[3:])
            if sem.isdigit():
                 result = get_syllabus(course.upper(), int(sem), subject)
                 if result["status"] == "success":
                     header = [
                         f"📚 Here is the syllabus for {subject}:",
                         f"Found it! Syllabus for {subject} (Sem {sem}):"
                     ]
                     reply_text = random.choice(header)
                     structured_data = result["data"]
                     data_type = "list"
                 else:
                     reply_text = f"⚠️ {result['message']}"
        if not reply_text: 
            ctx["awaiting"] = "syl_course"  # Fallback to context flow
            reply_text = "I didn't catch the details. Let's do it step-by-step. Which course?"

    # Direct Exam Command
    elif user_message.lower().startswith("exam"):
        parts = user_message.split()
        if len(parts) >= 3:
            course, sem = parts[1], parts[2]
            if sem.isdigit():
                result = get_exam_schedule(course.upper(), int(sem))
                if result["status"] == "success":
                     header = [
                         f"📝 Exam Schedule for {course} Sem {sem}:",
                         f"Get ready! Here are the exams for {course} Sem {sem}:"
                     ]
                     reply_text = random.choice(header)
                     structured_data = result["data"]
                     data_type = "table"
                else:
                    reply_text = f"⚠️ {result['message']}"
        if not reply_text: 
            ctx["awaiting"] = "exam_course" # Fallback to context flow
            reply_text = "Oops! Let's find your exams. Which course are you in?"


    # Default Fallback
    elif not reply_text:
        fallbacks = [
            "I can help with Attendance, Timetable, Syllabus, and Exam schedules.",
            "Try asking 'Check attendance' or 'Show timetable'.",
            "I'm here to assist with your academic queries. What do you need?"
        ]
        reply_text = random.choice(fallbacks)

    # Prepend Emotion Reply
    if emotion_reply:
         reply_text = f"{emotion_reply}\n{reply_text}"

    # 3. Translate Output to Target Language (if not English)
    final_reply = reply_text
    if target_lang != "en" and reply_text:
        try:
            print(f"DEBUG: Translating output '{reply_text}' from en -> {target_lang}")
            translator = GoogleTranslator(source='en', target=target_lang)
            translated = translator.translate(reply_text)
            if translated:
                final_reply = translated
                print(f"DEBUG: Translated output: {final_reply}")
            else:
                print("DEBUG: Translation returned empty, using original.")
        except Exception as e:
            print(f"ERROR: Output Translation Failed: {e}")

    response_payload = {"reply": final_reply}
    if structured_data:
        response_payload["data"] = structured_data
        response_payload["type"] = data_type

    return jsonify(response_payload)



def detect_emotion(msg):
    for emotion, keywords in EMOTIONS.items():
        if any(k in msg.lower() for k in keywords):
            return emotion
    return None

def log_conversation(message, intent, confidence):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO conversation_logs (message, intent, confidence, timestamp) VALUES (%s, %s, %s, %s)",
                    (message, intent, confidence, datetime.datetime.now()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logging error: {e}")

if __name__ == "__main__":
    app.run(debug=True)

