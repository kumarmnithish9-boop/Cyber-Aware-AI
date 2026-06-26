import os
import json
from google import genai

API_KEY =os.getnv("geminikey")

client = genai.Client(
    api_key=API_KEY
)

def generate_quiz():
  
    prompt = """
Generate exactly 4 cybersecurity Awareness MCQs, 3 Real time Cyber threat situations(mcq) and 3 cyber threat situations where user should be asked how would he react to it(mcq).

Rules:
1. Return exactly 10 questions.
2. Each question must have exactly 4 options.
3. Return valid JSON only.
4. Do not include markdown.
5. Include 2 to 3 line explanation field for every question.
6. Do not include any text outside the JSON array.
7. Questions should be of easy to moderate difficulty.


Example:

[
  {
    "question":"What is phishing?",
    "options":[
      "Virus",
      "Firewall",
      "Attempt to steal information",
      "Operating System"
    ],
    "answer":"Attempt to steal information",
    "explanation":"Phishing is a cyberattack that tricks users into revealing sensitive information."
  }
]

Do not include markdown.
Do not include explanations.
Return JSON only.
"""

 

    fallback_questions = [

    {
        "question": "What is phishing?",
        "options": [
            "A type of firewall",
            "A virus scanner",
            "An attempt to steal sensitive information",
            "An operating system"
        ],
        "answer": "An attempt to steal sensitive information",
        "explanation": "Phishing is a cyberattack where attackers trick users into revealing passwords, OTPs, or banking information through fake messages or websites."
    },

    {
        "question": "What does MFA stand for?",
        "options": [
            "Multiple File Access",
            "Main Firewall Access",
            "Multi-Factor Authentication",
            "Managed File Authentication"
        ],
        "answer": "Multi-Factor Authentication",
        "explanation": "MFA adds an extra layer of security by requiring more than one verification method before granting access."
    },

    {
        "question": "Which password is the strongest?",
        "options": [
            "123456",
            "password",
            "Nithish123",
            "T@9k#P2!xL7"
        ],
        "answer": "T@9k#P2!xL7",
        "explanation": "Strong passwords use a combination of uppercase letters, lowercase letters, numbers, and special characters."
    },

    {
        "question": "What should you do if you receive a suspicious email?",
        "options": [
            "Click all links",
            "Reply with personal details",
            "Delete or report it",
            "Forward it to everyone"
        ],
        "answer": "Delete or report it",
        "explanation": "Suspicious emails may contain phishing links or malware. It is safer to report or delete them."
    },

    {
        "question": "What is the purpose of a firewall?",
        "options": [
            "To monitor and filter network traffic",
            "To create passwords",
            "To store files",
            "To increase internet speed"
        ],
        "answer": "To monitor and filter network traffic",
        "explanation": "A firewall helps protect systems by controlling incoming and outgoing network traffic based on security rules."
    },

    {
        "question": "You receive a message saying your bank account will be suspended unless you click a link immediately. What should you do?",
        "options": [
            "Click the link immediately",
            "Provide account details",
            "Verify through the bank's official website",
            "Forward the message"
        ],
        "answer": "Verify through the bank's official website",
        "explanation": "Urgent messages asking for sensitive information are common phishing tactics. Always verify through official channels."
    },

    {
        "question": "A website asks for your OTP to claim a prize. What should you do?",
        "options": [
            "Share the OTP",
            "Ignore and leave the website",
            "Send OTP by email",
            "Call friends first"
        ],
        "answer": "Ignore and leave the website",
        "explanation": "Legitimate organizations never ask for OTPs to claim prizes. Sharing OTPs can compromise your accounts."
    },

    {
        "question": "You receive a USB drive from an unknown person. What is the safest action?",
        "options": [
            "Plug it into your computer",
            "Scan it with antivirus before use",
            "Share it with friends",
            "Upload all files online"
        ],
        "answer": "Scan it with antivirus before use",
        "explanation": "Unknown USB devices may contain malware. Always scan them before accessing any files."
    },

    {
        "question": "A colleague asks for your password to complete urgent work. What should you do?",
        "options": [
            "Share the password",
            "Share only part of it",
            "Refuse and follow security policy",
            "Write it on paper"
        ],
        "answer": "Refuse and follow security policy",
        "explanation": "Passwords should never be shared. Sharing credentials increases the risk of unauthorized access."
    },

    {
        "question": "While browsing, a pop-up claims your device is infected and asks you to install software. What should you do?",
        "options": [
            "Install it immediately",
            "Ignore it and close the pop-up",
            "Enter your password",
            "Share the alert on social media"
        ],
        "answer": "Ignore it and close the pop-up",
        "explanation": "Fake security alerts are commonly used to trick users into installing malware or revealing information."
    }

    ]

    try:

      response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
      )

      return json.loads(response.text)

    except Exception as e:

     print("Quiz Error:", e)

     return fallback_questions



    