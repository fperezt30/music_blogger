import json
import os
from google import genai
from groq  import Groq
from dotenv import load_dotenv


load_dotenv()

client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_gemini(prompt):
    try:
        response = client_gemini.models.generate_content(
            model="models/gemini-2.5-pro",
            contents=prompt
        )

        output_text = response.text.strip()

        # Clean markdown if present
        if output_text.startswith("```"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()

        return json.loads(output_text)
    
    except Exception as e:
        print("Gemini API error:", str(e))
        return {
            "error": True,
            "message": str(e)+" (Gemini API error)"}
    
def call_groq(prompt):
    try:
        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        output_text = response.choices[0].message.content.strip()

        # Clean markdown if present
        if output_text.startswith("```"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()

        return json.loads(output_text)
    
    except Exception as e:
        print("Groq API error:", str(e))
        return {
            "error": True,
            "message": str(e)+" (Groq API error)"}


    
def generate_with_fallback(prompt):
    
    groq_response = call_groq(prompt)

    if groq_response.get("error"):
        print("Falling back to Groq API...")
        return call_gemini(prompt)
    
    return groq_response