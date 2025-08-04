import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    """Extract meaningful content from a webpage."""
    try:
        response = requests.get(url, headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        soup = BeautifulSoup(response.content, 'html.parser')

        #extract key content
        title = soup.find('title').text if soup.find('title') else 'No title found'

        #get main text content
        content_tags = soup.find_all(['p', 'article', 'div'], class_ = lambda x: x and 'content' in x.lower())

        if not content_tags:
            content_tags = soup.find_all(['p']) #fallback to paragraphs if no specific content tags found
        content = ' '.join([tag.get_text().strip() for tag in content_tags[:10]]) #first 10 elements

        return {
            'url': url,
            'title': title,
            'content': content[:3000], #limit content to 3000 characters to avoid API limit
            'word_count': len(content.split())
        }
    except Exception as e:
        return {'error': str(e)}