# MentorMate AI 🚀  
Welcome to **MentorMate AI** — your terminal-based AI-powered mentor! This tool helps users explore job opportunities and get career/course guidance using conversational AI. It also includes resume analysis where users can upload their resume and ask questions about it.

Built with the **Google Gemini API** and **JSearch (via RapidAPI)**, it combines smart language understanding with real-time job data.

---

## 🌟 Features
- Terminal chatbot for job and course guidance  
- Resume upload with AI Q&A (PDF/Image)  
- Gemini-powered text and image analysis  
- JSearch integration for live job listings  

---

## 🛠️ Prerequisites
- Python 3.8+  
- pip (Python package manager)  
- Google API Key (Gemini)  
- RapidAPI Key (JSearch)  

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Subham0822/mentormate-ai
   cd mentormate-ai/mentor-chatbot-genai
   ```

2. **Set up virtual environment (optional)**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. ***Configure environment***

  - Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```
  - Add your keys:
  ```ini
    GOOGLE_API_KEY=your_google_gemini_key
    RAPIDAPI_KEY=your_rapidapi_jsearch_key
  ```

5. **Run the chatbot**
   ```bash
   python 1_app.py
   ```

6. **(Optional) Run Flask-based version**
   ```bash
   python app_flask.py
   ```

---

## 📁 Project Structure
```bash
mentor-chatbot-genai/
├── .env
├── .env.example
├── 1_app.py           # Main terminal chatbot
├── app_flask.py       # Optional Flask API version
└── requirements.txt
```

---

## 💬 Chat Capabilities
- Ask career advice, course suggestions, job roles  
- Gemini handles smart, context-aware replies  

---

## 🖼️ Resume QA Capabilities
- Upload resume (PDF/Image)  
- Ask:
  - “What are my strengths?”
  - “Suggest jobs based on my resume”
  - “Rewrite my experience section”

---

## 🔧 APIs Used

### 1. **Gemini API (Google)**  
- For chat and resume analysis  

### 2. **JSearch API (RapidAPI)**  
- Fetches live job listings based on queries  

---

## 🚀 Tips
- Use clear, concise resumes  
- Ask focused questions  
- Keep your `.env` keys secure  

---

## 🆘 Troubleshooting
- API key issues → Check `.env`  
- No job results? → Try a broader query  
- Errors? → Reinstall requirements:  
  ```bash
  pip install -r requirements.txt
  ```

--- 
