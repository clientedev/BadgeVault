import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse


def scrape_google_cloud_skills(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        name_elem = soup.find('h1', class_='profile-name')
        if not name_elem:
            name_elem = soup.find('h1')
        
        name = name_elem.get_text(strip=True) if name_elem else "Aluno"
        
        badge_elements = soup.find_all('div', class_='profile-badge')
        if not badge_elements:
            badge_elements = soup.find_all('img', alt=lambda x: x and 'badge' in x.lower())
        
        badge_count = len(badge_elements)
        
        if badge_count == 0:
            downloaded = trafilatura.fetch_url(url)
            text_content = trafilatura.extract(downloaded)
            if text_content:
                badge_count = text_content.lower().count('badge')
        
        return {
            'name': name,
            'badge_count': badge_count,
            'platform': 'Google Cloud Skills'
        }
    except Exception as e:
        raise Exception(f"Erro ao extrair dados do Google Cloud Skills: {str(e)}")


def scrape_profile(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    
    if not hostname:
        raise Exception("URL inválida. Por favor, insira um link válido do Google Cloud Skills.")
    
    hostname = hostname.lower()
    
    allowed_domains = [
        'skills.google',
        'www.skills.google',
        'cloudskillsboost.google',
        'www.cloudskillsboost.google'
    ]
    
    if hostname not in allowed_domains:
        raise Exception("Apenas perfis do Google Cloud Skills são suportados. Use links de cloudskillsboost.google ou skills.google.")
    
    if 'skills.google' in hostname or 'cloudskillsboost.google' in hostname:
        return scrape_google_cloud_skills(url)
    else:
        raise Exception("Apenas perfis do Google Cloud Skills são suportados.")
