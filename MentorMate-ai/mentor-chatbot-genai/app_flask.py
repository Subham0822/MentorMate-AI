import sys
import google.generativeai as genai
import json
import requests
import re
import os
from PIL import Image
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
messages = []

def save_chat_history(messages):
    return "\n\n".join([msg["content"] for msg in messages])

def generate_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return json.dumps({"error": f"API request failed: {str(e)}"})

def analyse_image_response(image: Image.Image, prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt, image])
    return response.text

def parse_json(response: str) -> dict:
    try:
        if response.startswith("```json") or response.startswith("```"):
            response = response[response.find("{") : response.rfind("}") + 1]
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {response}") from e

def get_intent(prompt: str) -> dict:
    intent_prompt = f"""You are an AI assistant specializing in providing advice related to careers, job opportunities, and job searches. Analyze the following prompt to determine the user's intent: "{prompt}"

    Return your analysis in JSON format with two fields:
    - "intent": Must be one of "career_guidance", "job_search", or "other"
    - "query": If intent is "job_search", extract the key search terms (e.g., job title, location, or industry). Otherwise, use null.

    Examples:
    "What skills should I learn to become a data scientist?" ->
    {{
        "intent": "career_guidance",
        "query": null
    }}

    "Can you help me find marketing jobs in Los Angeles?" ->
    {{
        "intent": "job_search",
        "query": "marketing, Los Angeles"
    }}

    "What’s the weather like today?" ->
    {{
        "intent": "other",
        "query": null
    }}

    "How do I prepare for a software engineering interview?" ->
    {{
        "intent": "career_guidance",
        "query": null
    }}

    "Find me remote graphic design jobs." ->
    {{
        "intent": "job_search",
        "query": "remote, graphic design"
    }}

    "Tell me a joke." ->
    {{
        "intent": "other",
        "query": null
    }}

    Respond only with valid JSON. 
    IMPORTANT: There should be NO text or backticks before or after the JSON."""
    
    response = generate_response(intent_prompt)
    return parse_json(response)

def get_image_intent(image: Image.Image) -> dict:
    prompt = """You are an AI assistant that identifies the type of an uploaded image.
    Determine whether the image is a 'resume' or 'other'.
    
    Return your response in JSON format:
    {
        "intent": "resume" or "other"
    }
    
    Respond only with valid JSON. There should be no text or backticks before or after the JSON."""
    
    response = analyse_image_response(image, prompt)
    return parse_json(response)

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")
    intent = get_intent(prompt)
    messages.append({"role": "user", "content": prompt})
    
    if intent["intent"] == "career_guidance":
        prompt = f"""You are an AI career mentor providing expert career guidance.
        The user asks: "{prompt}"
        Provide a well-structured and concise response in the following JSON format:
        {{
            "advice": "Your response here"
        }}
        Respond only with valid JSON. There should be no text or backticks before or after the JSON."""
        
        response = generate_response(prompt)
        final_response = parse_json(response)["advice"]
    
    elif intent["intent"] == "job_search":
        jobs = get_job_listings(intent["query"])
        prompt = f"""You are a job search assistant. The user is looking for jobs matching "{intent['query']}".
        The job listings found: "{jobs}"
        Provide a response in the given JSON format:
        {{
            "job_suggestions": "Your response here"
        }}
        Respond only with valid JSON. There should be no text or backticks before or after the JSON."""
        
        response = generate_response(prompt)
        final_response = parse_json(response)["job_suggestions"]
    else:
        final_response = generate_response(prompt)
    
    messages.append({"role": "assistant", "content": final_response})
    return jsonify({"response": final_response, "intent": intent})

@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image = Image.open(request.files["image"])
    prompt = request.form.get("prompt", "")
    context = save_chat_history(messages)
    img_prompt = f"{context}\n\n{prompt}"
    image_intent = get_image_intent(image)
    
    if image_intent["intent"] == "resume":
        resume_prompt = f"You are an AI resume expert. Analyze the following resume image and provide feedback on improvements.\n\nPrompt: {img_prompt}"
        response = analyse_image_response(image, resume_prompt)
    else:
        response = "Unsupported image type. Please upload a resume for analysis."
    
    messages.append({"role": "user", "content": img_prompt})
    messages.append({"role": "assistant", "content": response})
    return jsonify({"response": response})

API_KEY = os.getenv("RAPIDAPI_KEY")

def get_job_listings(query: str) -> str:
    query = re.sub(r"\s+", "+", query)
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    params = {"query": query, "page": "1", "num_pages": "1"}
    response = requests.get(url, headers=headers, params=params)
    job_items = []
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        for job in jobs[:3]:
            title = job.get("job_title", "Unknown Title")
            company = job.get("employer_name", "Unknown Company")
            location = job.get("location", "Unknown Location")
            link = job.get("job_apply_link", "#")
            job_items.append(f"• {title} at {company}, {location}\n  {link}")
    return "\n\n".join(job_items) if job_items else "No jobs found for this query."

@app.route("/get_jobs", methods=["GET"])
def get_jobs():
    query = request.args.get("query", "")
    response = get_job_listings(query)
    return jsonify({"job_listings": response})

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    global messages
    messages = []
    return jsonify({"message": "Chat history cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
