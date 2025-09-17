import io
import os
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
def extract(pdf_bytes: bytes) -> str:
    text = ""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text() 
    return text

def pdf_to_json(pdf_bytes: bytes) -> str:
    text = extract(pdf_bytes)
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts information from text and returns it as a valid JSON object. Only output the JSON object."
            },
            {
                "role": "user",
                "content": f"Please extract the key information from the following text and format it as a JSON object:\n\n{text}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )
    return completion.choices[0].message.content

def pdf_to_template(pdf_bytes: bytes, template: str = "modern") -> str:
    text = extract(pdf_bytes)
    client = Groq(api_key=API_KEY)

    prompt = f"""
    You are a resume formatting assistant.
    Take the following raw resume text and format it into a {template} resume style.
    Use clear headings (Name, Contact, Education, Experience, Skills, Projects).
    Return the result in Markdown format.
    Resume text:
    {text}
    """
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You format resumes into professional templates."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=4096,
        top_p=1,
        stream=False,
    )
    return completion.choices[0].message.content