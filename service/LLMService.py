import requests
import os


Groq_API = os.getenv("Groq_API")

def generate_book_brief(book_title: str , book_author: str , book_category: str):
    prompt = f"""   
    Generate a brief description of a book with the following details:
    Title: {book_title}
    Author: {book_author}
    Category: {book_category}
    """ 
    headers = {
        "Authorization": f"Bearer {Groq_API}",
        "Content-Type": "application/json"
    }
    json_payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=json_payload)
    
    if response.status_code != 200:
        raise Exception(f"Groq API Error: {response.text}")
        
    return response.json()["choices"][0]["message"]["content"]


    

    