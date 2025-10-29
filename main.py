import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# === Load API key from .env ===
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ Missing GEMINI_API_KEY in environment")

# === Configure Gemini ===
genai.configure(api_key=API_KEY)

# === FastAPI app ===
app = FastAPI(title="Gemini API Service", version="0.1.0")

# === Models ===
class Prompt(BaseModel):
    text: str

# === Root route ===
@app.get("/")
def root():
    return {"status": "ok", "message": "Gemini FastAPI service running"}

# === Simple "siema" test route ===
@app.get("/hello")
def hello():
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("siema, jak tam?")
    return {"response": response.text.strip()}

# === General prompt route ===
@app.post("/generate")
def generate(prompt: Prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt.text)
    return {"input": prompt.text, "response": response.text.strip()}
