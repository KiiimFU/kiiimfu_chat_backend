import cohere
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://kiiimfu.me"])

co = cohere.ClientV2(os.environ.get("Cohere_API"))

MESSAGE="""
You are an AI assistant representing Kimberly Fu's portfolio website.
Answer questions about her experience, projects, and skills based on her resume below.
Keep answers concise and friendly. If asked something unrelated to Kimberly, politely redirect.

--- RESUME ---

Kimberly Fu
Website: https://kiiimfu.me
Email: kimberlyfu006@gmail.com
GitHub: https://github.com/KiiimFU
LinkedIn: linkedin.com/in/kimberly-fu-99a634297

SKILLS
Technical: Python, Java, R, SQL, PostgreSQL, HTML, CSS, C, Git, Bash, JavaScript, MIPS Assembly, VS Code
Languages: English, Mandarin, Cantonese, Spanish (elementary)

EDUCATION
University of Toronto — Bachelor of Science, Computer Science Specialist (ASIP)
September 2023 – June 2028 (expected)
Relevant Courses: Software Design, Database, Data Structures, Machine Learning, Foundation of Computer Security, Artificial Intelligence

PROJECTS
- Survey-Based ML Random Forest Prediction Model (Python, Nov 2025): Trained on 825 survey responses, optimized 7 hyperparameters with Optuna, achieved 70.24% test accuracy.
- FamCalender (Personal Project, Oct 2025): PWA for real-time iCloud calendar sharing, integrated pyicloud, deployed on Render.
- Neurological Patient Care System (Hackathon, Feb 2025): MLP model with 90%+ accuracy on 11.5k EEG records from Kaggle, PostgreSQL database for healthcare providers and patients.
- Mystery Liquid (Ren'Py, April 2025): Visual novel crime scene simulation with branching logic and custom UI.
- Gear Up G1 Prep App (Java, Nov 2024): Study/test mode app built on SOLID principles with two GUIs.

WORK EXPERIENCE
Co-Founder / General Partner / Project Manager — Guangzhou Anchoracademy Education Consulting Co., Ltd. (June 2023 – Present)
- Leading development of an AI assistant decision model app (in progress).
- Co-founded the company, supported 350+ international students with university applications.

Teaching Assistant — University of Toronto Math Outreach (July 2024 – Present)
- Assists math/computer science instructor with class content.

LEADERSHIP & ACTIVITIES
- Events: 2024/2025 CAN-CWiC, 2025 WiAIG, NeuroHack
- Certificates: Google Cybersecurity Professional Certificate, ISC2 CC (both in progress)
- Captain: UofT Intramural Division 1 Mixed Basketball, District Basketball Team (7+ years)
- Coach/Founder: High School Women's Varsity Basketball Team

"""

@app.route("/chat", methods=["POST"])
def chat():
    # get data from frontend
    data = request.json
    user_message = data.get("message")
    user_history = data.get("history", [])
    # send to cohere, background + context + current prompt
    messages = [{"role": "system", "content": MESSAGE}] + user_history + [{"role": "user", "content": user_message}]
    res = co.chat(model="command-a-03-2025", messages=messages)

    response = res.message.content[0].text

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run()
