import requests
import json
from web_scraper import scrape_webpage
from config import OLLAMA_BASE_URL, MODEL_NAME

def analyze_with_llama(webpage_data):
    """Send webpage content to local Llama for analysis"""
    
    prompt = f"""Analyze this webpage content and suggest what I should note about it:

URL: {webpage_data['url']}
Title: {webpage_data['title']}
Content: {webpage_data['content'][:2000]}

Please provide:
1. Key takeaways (2-3 points)
2. Notable people or companies mentioned  
3. Should I reach out or follow up? Why?
4. Tags for categorization

Keep response concise and actionable."""
    
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", 
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def main():
    print("🦙 LinkedIn Note Agent (Powered by Llama)")
    url = input("\nEnter LinkedIn article URL: ")
    
    print("\n🔍 Scraping webpage...")
    webpage_data = scrape_webpage(url)
    
    if 'error' in webpage_data:
        print(f"❌ Error: {webpage_data['error']}")
        return
    
    print(f"📄 Found: {webpage_data['title']}")
    print(f"📝 Content length: {webpage_data['word_count']} words")
    
    print(f"\n🤖 Analyzing with {MODEL_NAME}...")
    analysis = analyze_with_llama(webpage_data)
    print("\n" + "="*50)
    print("📋 AI ANALYSIS:")
    print("="*50)
    print(analysis)
    print("="*50)

if __name__ == "__main__":
    main()