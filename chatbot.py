import os
from google import genai

API_KEY = os.getenv("geminikey")

client = genai.Client(api_key=API_KEY)

def get_response(user_question):

    prompt = f"""
    You are CyberAware AI.

    Rules:
    1. Answer ONLY cybersecurity-related questions.
    2. Topics include phishing, malware, ransomware, passwords, MFA, firewalls, privacy, cyber attacks, online safety and cybersecurity awareness.
    3. If the question is not related to cybersecurity, reply:
       "I can only answer cybersecurity-related questions."
    4. Keep answers simple and educational.

    User Question:
    {user_question}
    """

    try:

        response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
        )

        return response.text

    except Exception as e:
      
       print("Chatbot Error:", e)

       return "AI service is currently unavailable."
        