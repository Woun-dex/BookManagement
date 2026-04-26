import requests
import os


Groq_API = os.getenv("Groq_API")

def generate_book_brief(book_title: str , book_author: str , book_category: str):
    prompt = f"""   
    Write a brief, engaging description (1 paragraph) for the book '{book_title}' by {book_author} in the {book_category} category.
    Do not include any boilerplate text like 'Here is a brief description', do not include the title, author, or category labels. Just output the description itself in plain text.
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


    

    