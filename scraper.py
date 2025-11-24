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


def scrape_credly(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        name_elem = soup.find('h1', class_='profile-name')
        if not name_elem:
            name_elem = soup.find('h1')
            if not name_elem:
                name_elem = soup.find('div', class_='cr-profile-header__title')
        
        name = name_elem.get_text(strip=True) if name_elem else "Aluno"
        
        badge_elements = soup.find_all('div', class_='cr-badge')
        if not badge_elements:
            badge_elements = soup.find_all('a', href=lambda x: x and '/badges/' in x)
        
        badge_count = len(badge_elements)
        
        if badge_count == 0:
            count_elem = soup.find('span', class_='profile-badge-count')
            if count_elem:
                try:
                    badge_count = int(count_elem.get_text(strip=True))
                except:
                    pass
        
        return {
            'name': name,
            'badge_count': badge_count,
            'platform': 'Credly'
        }
    except Exception as e:
        raise Exception(f"Erro ao extrair dados do Credly: {str(e)}")


def scrape_profile(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    if 'credly.com' in domain:
        return scrape_credly(url)
    elif 'skills.google' in domain or 'cloudskillsboost.google' in domain:
        return scrape_google_cloud_skills(url)
    else:
        raise Exception("Plataforma não suportada. Use links do Google Cloud Skills ou Credly.")
