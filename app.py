import streamlit as st
import db
import ai_quiz
import phishing
import pytesseract
import chatbot
import qr_detector
import pandas as pd
import sqlite3
from PIL import Image
import background
import time
import virustotal
import re
import os

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

st.set_page_config(
    page_title="CyberAware AI",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if "show_splash" not in st.session_state:
    st.session_state.show_splash = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False    

if "verified" not in st.session_state:
    st.session_state.verified = False

if "show_result" not in st.session_state:
    st.session_state.show_result = False    

if "menu_choice" not in st.session_state:
    st.session_state.menu_choice = "Dashboard"    
if st.session_state.show_splash:

    background.set_background("images/welcome_banner.png")
    st.markdown("""
        <h1 style='text-align:center;color:#00FF99;'>
        🛡 CyberAware AI
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style='text-align:center;color:white;font-size:18px;'>
        Learn • Detect • Protect
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            "<h2 style='text-align:center;color:#00FF99;'>Loading CyberAware AI...</h2>",
            unsafe_allow_html=True
        )

        progress = st.progress(0)
     
        st.caption("Initializing AI modules...")
        for i in range(101):

            progress.progress(i)

            time.sleep(0.03)

    st.session_state.show_splash = False

    st.rerun()


db.create_database()


def footer():
        st.markdown(
            """
            <div style="
            position:fixed;
            bottom:12px;
            width:100%;
            text-align:center;
            color:gray;
            font-size:12px;
            ">

            © 2026 CyberAware AI | MCA Mini Project

            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("""
    <style>


    [data-testid="stSidebar"] {
        background-color: #101827;
    }

    h1, h2, h3 {
        color: #00FF99;
    }

    p, label, div {
        color: white;
    }

    .stButton > button {

        background-color: #111827;

        color: #E5E7EB;

        border: 1px solid #374151;

        border-radius: 8px;

        width: 100%;

        font-weight: 500;

        transition: all 0.3s ease;
    }

    .stButton > button:hover {

        background-color: #1F2937;

        border: 1px solid #00FF99;

        color: white;
    }
    .stTextInput input,
    .stTextArea textarea {

        background-color: #161B22;

        color: white;

        border-radius: 10px;
    }

    hr {

        border-color: #00FF99;
    }
    /* Glass Container */

    .glass-card{

        background: rgba(15,23,42,0.75);

        border:1px solid rgba(255,255,255,0.08);

        border-radius:18px;

        padding:25px;

        backdrop-filter:blur(14px);

        -webkit-backdrop-filter:blur(14px);

        box-shadow:0 8px 32px rgba(0,0,0,0.35);

        margin-bottom:20px;
    }
            
    img{

    border-radius:18px;

    box-shadow:0px 8px 25px rgba(0,0,0,0.35);
    }

    </style>
    """, unsafe_allow_html=True)


if st.session_state.logged_in:

    if st.session_state.is_admin:

        menu = [
            "🛡 Admin Dashboard"
        ]

    else:

        menu = [
            "🏠 Dashboard",
            "🧠 AI Quiz",
            "📊 Quiz History",
            "🎣 Phishing Simulator",
            "📱 QR Scam Detector",
            "🤖 AI Chatbot"
        ]

else:

    menu = [
        "🔐 Login",
        "📝 Register",
        "🔑 Forgot Password"
    ]

col1, col2, col3 = st.sidebar.columns([1,2,1])

with col2:
    st.image(
        "images/logo.png",
        width=120
    )
st.sidebar.markdown("""
<div style='text-align:center;'>

<h2 style='color:#00FF99;'>
CyberAware AI
</h2>

<p style='color:white;'>
Stay Alert. Stay Secure.
</p>

</div>
""", unsafe_allow_html=True)

choice = st.sidebar.radio(
    "Menu",
     menu,
     index=0
)

if st.session_state.logged_in:

    st.sidebar.markdown(
    "<div style='height:120px'></div>",
    unsafe_allow_html=True
)

    st.sidebar.markdown("---")

    logout_btn = st.sidebar.button(
        "🚪 Logout"
    )
   

    delete_btn = st.sidebar.button(
        "🗑 Delete Account"
    )

    if logout_btn:

        st.toast("👋 Logged out successfully!")

        st.session_state.logged_in = False

        time.sleep(1)

        st.rerun()

    if delete_btn:

        st.session_state.menu_choice = "Delete Account"

        choice = "Delete Account"  

    

if choice == "🔐 Login":

    background.set_background(
        "images/welcome_banner.png"
    )
    st.markdown("""
        <h1 style='text-align:center;color:#00FF99;'>
        🛡 CyberAware AI
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style='text-align:center;color:white;font-size:18px;'>
        Learn • Detect • Protect
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("🔐 Secure Login")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )
    
        if st.button("Login"):

            if db.is_account_locked(username):

                st.error(
                    "Account is locked. Try again after 1 hour."
                )

            else:
               

                # ---------------- ADMIN LOGIN ---------------- #

                if (
                    username == ADMIN_USERNAME
                    and
                    password == ADMIN_PASSWORD
                ):
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.session_state.username = "admin"

                    st.success(
                        "Welcome Admin!"
                    )

                    st.rerun()

                # ---------------- NORMAL USER LOGIN ---------------- #

                else:

                    user = db.login_user(
                        username,
                        password
                    )

                    if user:

                        db.reset_failed_attempts(
                            username
                        )

                        st.session_state.logged_in = True
                        st.session_state.is_admin = False
                        st.session_state.username = username

                        st.success(
                            "Login Successful!"
                        )

                        st.rerun()

                    else:

                        db.record_failed_login(
                            username
                        )

                        conn = sqlite3.connect("users.db")
                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            SELECT failed_attempts
                            FROM users
                            WHERE username = ?
                            """,
                            (username,)
                        )

                        result = cursor.fetchone()

                        conn.close()

                        if result:

                            attempts = result[0]

                            if attempts >= 5:

                                st.error(
                                    "Too many failed attempts. Account locked for 1 hour."
                                )

                            else:

                                st.error(
                                    f"Invalid Username or Password. Attempts left: {5 - attempts}"
                                )

                        else:

                            st.error(
                                "Invalid Username or Password"
                            )

        footer()

elif choice == "📝 Register":

    background.set_background(
        "images/welcome_banner.png"
    )
    st.markdown("""
        <h1 style='text-align:center;color:#00FF99;'>
        🛡 CyberAware AI
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style='text-align:center;color:white;font-size:18px;'>
        Learn • Detect • Protect
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📝 Create Account")
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        answer1 = st.text_input("What is your favourite book?")
        answer2 = st.text_input("What is your favourite movie?")
        answer3 = st.text_input("What is your favourite holiday destination?")
        if st.button("Register"):

            if username.strip() == "" or password.strip() == "":
                st.error("Username and Password cannot be empty")

            elif not db.is_strong_password(password):

                st.warning(
                    "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character."
                )
        

            else:
                try:
                    db.add_user(username, password, answer1, answer2, answer3)
                    st.success("User Registered Successfully!")

                except Exception:
                    st.error("Username already exists!")
        footer()


elif choice == "🔑 Forgot Password":

    background.set_background(
        "images/welcome_banner.png"
    )
    st.markdown("""
        <h1 style='text-align:center;color:#00FF99;'>
        🛡 CyberAware AI
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style='text-align:center;color:white;font-size:18px;'>
        Learn • Detect • Protect
        </p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🔑 Reset Password")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:

        username = st.text_input("Username")

        a1 = st.text_input("What is your favourite book?")
        a2 = st.text_input("What is your favourite movie?")
        a3 = st.text_input("What is your favourite holiday destination?")

        if st.button("Verify"):

            if db.verify_security_answers(
                username,
                a1,
                a2,
                a3
            ):
                st.session_state.verified = True
                st.success("Verification Successful")

            else:
                st.session_state.verified = False
                st.error("Wrong Answers")

        if st.session_state.verified:

            new_password = st.text_input(
                "New Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            if st.button("Reset Password"):
    
             if new_password != confirm_password:

                st.error(
                "Passwords do not match"
                )

             elif not db.is_strong_password(
                new_password
                ):

                st.warning(
                "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character."
                )

            else:

                db.reset_password(
                    username,
                    new_password
                )

                st.success(
                    "Password Reset Successfully!"
                )

                st.session_state.verified = False       
        footer()

elif choice == "🏠 Dashboard":

    background.set_background(
    "images/dashboard_banner.png"
    )

    hero_col1, hero_col2 = st.columns([2,1])

    with hero_col1:

        st.markdown(f"""
            <div class="glass-card">

            <h2 style="color:#00FF99;">
            🛡 Welcome, {st.session_state.username}
            </h2>

            <p style="font-size:18px;color:white;">
            Your cybersecurity learning dashboard.
            Monitor your quiz performance, practice
            against phishing attacks and improve your
            digital safety.
            </p>

            </div>
            """, unsafe_allow_html=True)

    with hero_col2:

        st.image(
        "images/shield_3d.png",
        width=300
         )

        scores = db.get_scores(
            st.session_state.username
          )

    if scores:

        total_attempts = len(scores)

        best_score = max(
            score[0]
            for score in scores
        )

        latest_score = scores[-1][0]

        average_score = sum(
            score[0]
            for score in scores
        ) / total_attempts

        st.subheader(
         "📊 Performance Summary"
          )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.info(
                f"""
        📊 Attempts

        ## {total_attempts}
        """
            )

        with col2:

            st.info(
                f"""
        🏆 Best Score

        ## {best_score}
        """
            )

        with col3:

            st.info(
                f"""
        🎯 Latest Score

        ## {latest_score}
        """
            )

        with col4:

            st.info(
                f"""
        📈 Average

        ## {round(average_score, 2)}
        """
            )
        
        st.markdown("---")

        st.subheader(
            "📈 Quiz Performance Overview"
        )

        df = pd.DataFrame(
            {
                "Attempt": range(
                    1,
                    total_attempts + 1
                ),
                "Score": [
                    score[0]
                    for score in scores
                ]
            }
        )

        st.line_chart(
            df.set_index(
                "Attempt"
            )
        )

        st.markdown("---")

        st.info(
            "🔒 Cyber Tip: Never share OTPs, passwords, or verification codes with anyone."
        )

    else:

        st.info(
            "🚀 Take your first quiz to start tracking your cybersecurity progress."
        )
elif choice == "🧠 AI Quiz":
    background.set_background(
    "images/quiz_banner.png"
    )

    st.markdown("""
        <div class="glass-card">

        <h3 style="color:#00FF99;">
        🧠 AI Cybersecurity Quiz
        </h3>

        <p>
        Generate AI-powered cybersecurity questions,
        test your knowledge and receive explanations
        for incorrect answers.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.subheader("🚀 Start Quiz")

    if st.button("Generate Quiz"):

      if "quiz" not in st.session_state:

         with st.spinner("🧠 Generating AI Quiz..."):

            quiz = ai_quiz.generate_quiz()

         if quiz:

            st.session_state.quiz = quiz

         else:

            st.error(
                "Quiz generation unavailable. Gemini quota exceeded."
            )
        

    if "quiz" in st.session_state:

        user_answers = []

        for i, q in enumerate(st.session_state.quiz):

           with st.container(border=True):

                st.subheader(
                    f"Question {i+1}"
                )

                answer = st.radio(
                    q["question"],
                    q["options"],
                    key=f"q{i}",
                    index=None
                )

           user_answers.append(answer)

        if st.button("Submit Quiz"):

           if None in user_answers:

              st.error(
                 "Please answer all questions before submitting."
              )

           else:

                score = 0

                wrong_questions = []

                for i, q in enumerate(st.session_state.quiz):

                    if user_answers[i] == q["answer"]:

                         score += 1

                    else:

                        wrong_questions.append(
                        {
                            "question": q["question"],
                            "your_answer": user_answers[i],
                            "correct_answer": q["answer"],
                            "explanation": q["explanation"]
                        }
                        )

                st.session_state.score = score
                st.session_state.wrong_questions = wrong_questions
                st.session_state.show_result = True

                db.save_score(
                  st.session_state.username,
                  score,
                  len(st.session_state.quiz)
                )

        if st.session_state.show_result:

           with st.container(border=True):

            st.header("Quiz Result")

            st.write(
                f"User: {st.session_state.username}"
            )

            st.write(
                f"Score: {st.session_state.score}/{len(st.session_state.quiz)}"
            )

            if st.session_state.score >= 7:

                st.success("Performance: Excellent")

                st.balloons()


            elif st.session_state.score >= 5:

                st.info("Performance: Good")

            else:

                st.warning("Performance: Needs Improvement")

            st.write(
                f"Correct Answers: {st.session_state.score}"
            )

            st.write(
                f"Wrong Answers: {len(st.session_state.wrong_questions)}"
            )

           if st.button("Explain Wrong Answers"):

             
                for q in st.session_state.wrong_questions:

                  st.subheader("Question")

                  st.write(q["question"])

                  st.write(
                    f"Your Answer: {q['your_answer']}"
                  )

                  st.write(
                    f"Correct Answer: {q['correct_answer']}"
                  )

                  st.info(
                     q["explanation"]
                  )

                  st.divider()
           if st.button("Clear"):

                 st.session_state.show_result = False

                 if "quiz" in st.session_state:
                    del st.session_state.quiz

                 
                 if "wrong_questions" in st.session_state:
                    del st.session_state.wrong_questions
    

                 for i in range(10):
                      key = f"q{i}"

                      if key in st.session_state:
                         del st.session_state[key]

                 st.rerun()        

elif choice == "📊 Quiz History":
    background.set_background(
    "images/dashboard_banner.png"
    )

    st.markdown("""
    # 📊 Quiz History

    ### Track Your Cybersecurity Learning Journey
    """)

    scores = db.get_scores(
        st.session_state.username
    )

    if scores:

        total_attempts = len(scores)

        best_score = max(
            score[0]
            for score in scores
        )

        average_score = sum(
            score[0]
            for score in scores
        ) / total_attempts

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"""
            📚 Attempts

            ## {total_attempts}
            """
                        )

        with col2:

            st.info(
                f"""
                🏆 Best Score

                ## {best_score}
                """
                            )

        with col3:

            st.info(
                f"""
            📈 Average

            ## {round(average_score, 2)}    
            """
                        )

        st.markdown("---")

        st.subheader(
            "📋 Attempt History"
        )

        history_data = []

        for i, score in enumerate(scores):

            history_data.append(
                {
                    "Attempt": i + 1,
                    "Score": score[0],
                    "Total": score[1]
                }
            )

        df = pd.DataFrame(
            history_data
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "📈 Progress Trend"
        )

        chart_df = pd.DataFrame(
            {
                "Attempt": range(
                    1,
                    total_attempts + 1
                ),
                "Score": [
                    score[0]
                    for score in scores
                ]
            }
        )

        st.line_chart(
            chart_df.set_index(
                "Attempt"
            )
        )

    else:

        st.info(
            "🚀 Complete your first quiz to see your history."
        )
        
elif choice == "🎣 Phishing Simulator":
    background.set_background(
    "images/phishing_banner.png"
    )

    st.markdown("""
        <div class="glass-card">

        <h3 style="color:#00FF99;">
        🎣 Phishing Simulator
        </h3>

        <p>

        Paste an email or upload a screenshot or URL.

        Our AI detects phishing indicators,
        suspicious links and social engineering attacks.

        </p>

        </div>
        """, unsafe_allow_html=True)

    st.subheader(
        "📥 Message Input"
    )

    email_text = st.text_area(
        "Paste Email or Message or URL",
        key="email_input"
    )

    st.subheader(
        "🖼 Upload Image"
    )

    extracted_text = ""

    uploaded_file = st.file_uploader(
        "Upload Email or URL Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Screenshot"
        )

        extracted_text = pytesseract.image_to_string(
            image
        )

        st.subheader(
            "🔍 Extracted Text"
        )

        st.text_area(
            "Detected Text",
            extracted_text,
            height=200,
            key="ocr_text"
        )

    st.markdown("---")

    st.subheader(
        "🚀 Start Analysis"
    )

    if st.button("Analyze"):

        text_to_check = email_text

        if uploaded_file is not None:
            text_to_check = extracted_text

        with st.spinner("🔍 Analyzing Email..."):

            score, reasons = phishing.check_phishing(
                text_to_check
            )
        url_match = re.search(
             r'((https?://)?(www\.)?([A-Za-z0-9-]+\.)+[A-Za-z]{2,}(/[^\s]*)?)',
            text_to_check
        )

        vt_result = None

        if url_match:

            url = url_match.group()
        if not url.startswith(("http://", "https://")):

            url = "https://" + url

            st.info(f"🌐 URL Detected: {url}")
            with st.spinner("🛡 Checking URL with VirusTotal..."):

                vt_result = virustotal.check_url(url)    

        if score >= 4:

                    st.error(
                        "Risk Level: HIGH"
                    )

        elif score >= 2:

            st.warning(
                "Risk Level: MEDIUM"
            )

        else:

            st.success(
                "Risk Level: LOW"
            )

        st.subheader(
            "📋 Detection Reasons"
        )

        if reasons:

          for reason in reasons:

            st.info(reason)

        else:
 
            st.success(
                "No suspicious indicators detected."
            )
        if vt_result:

            st.markdown("---")

            st.subheader("🛡 VirusTotal Scan")

            st.write(
                f"🟢 Harmless : {vt_result['harmless']}"
            )

            st.write(
                f"🔴 Malicious : {vt_result['malicious']}"
            )

            st.write(
                f"🟡 Suspicious : {vt_result['suspicious']}"
            )

            st.write(
                f"⚪ Undetected : {vt_result['undetected']}"
            )

            if vt_result["malicious"] > 0:

                st.error(
                    "❌ This URL has been flagged as malicious by security vendors. Do NOT open it."
                )

            elif vt_result["suspicious"] > 0:

                st.warning(
                    "⚠ Some vendors consider this URL suspicious. Proceed with caution."
                )

            else:

                st.success(
                    "✅ No malicious detections found by VirusTotal."
        )
elif choice == "🤖 AI Chatbot":
    background.set_background(
    "images/chatbot_banner.png"
    )

    st.markdown("""
        <div class="glass-card">

        <h3 style="color:#00FF99;">
        🤖 Cybersecurity Assistant
        </h3>

        <p>

        Ask cybersecurity questions anytime.

        Learn about phishing, malware,
        passwords, ransomware,
        social engineering and more.

        </p>

        </div>
        """, unsafe_allow_html=True)
    
    st.subheader(
        "💬 Ask Your Question"
    )
    user_question = st.text_input(
        "Ask a cybersecurity question"
    )

    if st.button("Ask"):

     if user_question.strip() == "":

        st.warning(
            "Please enter a cybersecurity question."
        )

     else:

        with st.spinner("🤖 Thinking..."):

            answer = chatbot.get_response(
                user_question
            )

        st.subheader(
            "🤖 AI Response"
        )

        st.success(answer)        

elif choice == "📱 QR Scam Detector":
    background.set_background(
    "images/qr_banner.png"
    )

    st.markdown("""
        <div class="glass-card">

        <h3 style="color:#00FF99;">
        📱 QR Scam Detector
        </h3>

        <p>

        Upload or scan a QR code.

        The system extracts the QR content and
        checks it for phishing and malicious URLs.

        </p>

        </div>
        """, unsafe_allow_html=True)
    
    st.subheader(
      "📥 Choose Input Method"
    )

    method = st.radio(
        "Select Input Method",
        ["Upload QR Image", "Scan Using Camera"]
    )

    image = None

    if method == "Upload QR Image":

        qr_file = st.file_uploader(
            "Upload QR Code",
            type=["png", "jpg", "jpeg"]
        )

        if qr_file is not None:

            image = Image.open(qr_file)

    else:

        camera_image = st.camera_input(
            "Scan QR Code"
        )

        if camera_image is not None:

            image = Image.open(camera_image)

    st.markdown("---")

    st.subheader(
            "🔍 QR Analysis"
        )       

    if image is not None:

        st.image(
            image,
            caption="QR Code"
        )

        with st.spinner("📱 Scanning QR Code..."):

            qr_text = qr_detector.read_qr(image)

        if qr_text == "No QR code detected":

            st.error(
                "No QR code detected in the image."
            )

        else:

            st.subheader("📄QR Content")

            st.code(qr_text)

            with st.spinner("🛡 Checking QR Safety..."):

                score, reasons = phishing.check_phishing(
                    qr_text
                )

            if score >= 4:

                st.error(
                    "Risk Level: HIGH"
                )

            elif score >= 2:

                st.warning(
                    "Risk Level: MEDIUM"
                )

            else:

                st.success(
                    "Risk Level: LOW"
                )

            st.subheader("📋 Detection Reasons")

            if reasons:

                for reason in reasons:

                    st.info(reason)

            else:

                st.info(
                     "No suspicious indicators detected."
                )

elif choice == "Delete Account":

    background.set_background(
        "images/welcome_banner.png"
    )

    st.header("Delete Account")

    st.warning(
        "This action cannot be undone."
    )

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Delete My Account"):

        user = db.login_user(
            st.session_state.username,
            password
        )

        if user:

            db.delete_user(
                st.session_state.username
            )

            st.success(
                "Account deleted successfully."
            )

            st.session_state.logged_in = False

            st.rerun()

        else:

            st.error(
                "Incorrect password."
            )                

    footer()            