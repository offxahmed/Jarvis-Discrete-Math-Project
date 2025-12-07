from googlesearch import search
from groq import Groq
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def google_search(query, num_results=3):
    """Perform Google search and extract content"""
    results = []
    
    try:
        for url in search(query, num_results=num_results):
            try:
                response = requests.get(url, timeout=3)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract text content
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text() for p in paragraphs[:5]])
                
                results.append({
                    'url': url,
                    'content': content[:500]  # Limit content length
                })
            except:
                continue
                
    except Exception as e:
        print(f"Search error: {e}")
    
    return results

def real_time_search(query):
    """Search internet and generate answer using LLM"""
    
    # Perform Google search
    search_results = google_search(query)
    
    if not search_results:
        return "I couldn't find relevant information on the internet."
    
    # Combine search results
    context = "\n\n".join([f"Source: {r['url']}\n{r['content']}" for r in search_results])
    
    # Generate answer using LLM with search context
    messages = [
        {"role": "system", "content": f"You are Jarvis. Answer the user's question using the provided search results. Be accurate and cite sources when possible. Current date: {datetime.now().strftime('%B %d, %Y')}"},
        {"role": "user", "content": f"Question: {query}\n\nSearch Results:\n{context}"}
    ]
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.5,
        max_tokens=800
    )
    
    return response.choices[0].message.content
