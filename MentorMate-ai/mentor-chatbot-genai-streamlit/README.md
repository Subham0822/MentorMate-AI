# MentorMate AI 🚀
Welcome to MentorMate AI — your personal AI-powered mentor! This application is designed to help users explore job opportunities and receive guidance on career paths and course selection using conversational AI. It also includes an image analysis feature where users can upload their resume and ask questions about it.

Built using Google Gemini API and JSearch (via RapidAPI), this tool combines powerful language understanding with real-time job data for a seamless mentorship experience.

## 🌟 Features
- Conversational chatbot for job and course guidance

- Resume upload with AI-powered Q&A

- Gemini-powered text and image analysis

- JSearch integration for live job results

- Clean UI with Streamlit

## 🛠️ Prerequisites
- Python 3.8+

- pip (Python package manager)

- Google API Key (Gemini)

- RapidAPI Key (JSearch)

🚀 Getting Started
1. ***Clone the repository***

    ```bash
    git clone https://github.com/Subham0822/mentormate-ai
    cd mentormate-ai/mentor-chatbot-genai-streamlit
    ```
    
2. ***Set up virtual environment (optional)***

    ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```
3. ***Install dependencies***

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

5. ***Run the application***

  ```bash
  streamlit run Home.py
  ```

6. ***📁 Project Structure***

  ```bash
  mentor-chatbot-genai-streamlit/
  ├── assets/
  │   └── build.jpeg
  ├── components/
  │   ├── __init__.py
  │   └── mentor.py
  ├── pages/
  │   ├── 1_Chat.py
  │   └── 2_Image_Analysis.py
  ├── tools/
  │   ├── __init__.py
  │   └── mentor.py
  ├── utils/
  │   ├── __init__.py
  │   ├── generate.py
  │   └── parse.py
  ├── .env
  ├── Home.py
  └── requirements.txt

  ```

## 💬 Chat Section***

- Ask about career advice, course suggestions, or job roles.

- Gemini handles context-aware conversation.

## 🖼️ Resume QA Section
- Upload your resume (PDF/Image)

- Ask questions like:

  - “What are my strengths based on this resume?”

  - “Suggest roles for me based on this resume”

  - “Rewrite my experience in concise format”

## 🔧 APIs Used
1. ***Gemini API (Google)***

  - Text and image analysis

  - Intelligent responses to chat and resume inputs

2. ***JSearch API (RapidAPI)***

Real-time job listings based on user input

## 🚀 Tips
- Keep resumes clear for better analysis

- Ask specific questions for actionable insights

- Use secure .env for your API keys

## 🆘 Troubleshooting
- Key errors? → Check your .env file

- No job results? → Refine your query

- Module errors? → Run pip install -r requirements.txt
