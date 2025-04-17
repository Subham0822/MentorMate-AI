import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import requests
import re
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text


def analyse_image_response(image: Image.Image, prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt, image])
    return response.text

import json


def parse_json(response: str) -> dict:
    if response.startswith("```json") or response.startswith("```"):
        response = response[len("```json") or len("```") :]
    if response.endswith("```"):
        response = response[: -len("```")]
    return json.loads(response)

def get_intent(prompt: str) -> dict:
    """
    Determines if the prompt is related to career guidance, job search, or other topics.
    """
    prompt = f"""You are an AI assistant specializing in providing advice related to careers, job opportunities, and job searches. Analyze the following prompt to determine the user's intent: "{prompt}"

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

    response = generate_response(prompt)
    return parse_json(response)

def generate(prompt: str) -> str:
    """
    Handles career-related queries and generates appropriate responses.
    """
    intent = get_intent(prompt)

    if intent["intent"] == "career_guidance":
        prompt = f"""You are an AI career mentor providing expert career guidance.
        The user asks: "{prompt}"
        Provide a well-structured and concise response in the following JSON format:
        {{
            "advice": "Your response here"
        }}
        Respond only with valid JSON. There should be no text or backticks before or after the JSON."""

        response = generate_response(prompt)
        return parse_json(response)["advice"]

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
        return parse_json(response)["job_suggestions"]

    else:
        return generate_response(prompt)

def get_image_intent(image: Image.Image) -> dict:
    """
    Determines whether the uploaded image is a resume or something else.
    """
    prompt = """You are an AI assistant that identifies the type of an uploaded image.
    Determine whether the image is a 'resume' or 'other'.
    
    Return your response in JSON format:
    {
        "intent": "resume" or "other"
    }

    Respond only with valid JSON. There should be no text or backticks before or after the JSON."""

    response = analyse_image_response(image, prompt)
    return parse_json(response)

def get_text_intent(prompt: str) -> dict:
    """
    Determines whether the prompt is related to image analysis, a casual greeting, or something else.
    """
    prompt = f"""You are an AI assistant analyzing user intent.
    Determine if the following prompt is related to 'image_analysis', 'greeting', or 'other'.

    User prompt: "{prompt}"

    Return the result in JSON format:
    {{
        "intent": "image_analysis" or "greeting" or "other"
    }}

    Respond only with valid JSON. There should be no text or backticks before or after the JSON."""

    response = generate_response(prompt)
    return parse_json(response)

def analyse_image(image: Image.Image, prompt: str) -> str:
    """
    Analyzes an image based on the given prompt, but also handles greetings and unrelated messages properly.
    """
    text_intent = get_text_intent(prompt)

    if text_intent["intent"] == "greeting":
        return "Hello! How can I assist you today?"

    elif text_intent["intent"] == "other":
        return "I can analyze resumes. Please upload a resume for review."

    else:  # If it's related to image analysis
        image_intent = get_image_intent(image)

        if image_intent["intent"] == "resume":
            resume_prompt = f"You are an AI resume expert. Analyze the following resume image and provide feedback on any improvements, refinements, or upgrades needed. If the resume is well-structured with no major issues, respond with 'It is all good'. Resume feedback should focus on formatting, clarity, relevant skills, and industry standards.\n\nPrompt: {prompt}"
            return analyse_image_response(image, resume_prompt)
        
        else:
            return "Unsupported image type. Please upload a resume for analysis."

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

def get_job_listings(query: str) -> str:
    query = re.sub(r"\s+", "+", query)

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,  # Replace with your actual API key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

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

def save_chat_history(messages):
    return "\n\n".join([msg["content"] for msg in messages])

def main():
    messages = []
    print("AI Assistant - Chat & Image Analysis")
    print("Type 'clear' to clear the chat, 'image' to analyze an image, or 'exit' to quit.")
    
    while True:
        prompt = input("You: ")
        
        if prompt.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break
        
        elif prompt.lower() == "clear":
            messages = []
            print("Chat cleared.")
            continue
        
        elif prompt.lower() == "image":
            image_path = input("Enter image file path: ")
            try:
                image = Image.open(image_path)
                image.show()
            except Exception as e:
                print(f"Error loading image: {e}")
                continue
            
            img_prompt = input("Describe what you want analyzed: ")
            context = save_chat_history(messages)
            img_prompt = f"{context}\n\n{img_prompt}"
            response = analyse_image(image, img_prompt)
            print("\nAnalysis:", response)
            messages.append({"role": "user", "content": img_prompt})
            messages.append({"role": "assistant", "content": response})
            continue
        
        messages.append({"role": "user", "content": prompt})
        context = save_chat_history(messages)
        prompt = f"{context}\n\n{prompt}"
        response = generate(prompt)
        print("\nResponse:", response)
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()