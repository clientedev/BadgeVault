import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob


def get_selenium_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--no-first-run')
        
        chromium_paths = glob.glob('/nix/store/*-chromium-*/bin/chromium')
        if chromium_paths:
            chrome_options.binary_location = chromium_paths[0]
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        raise Exception(
            f"Erro ao inicializar Chrome WebDriver: {str(e)}. "
            "Certifique-se de que Chrome/Chromium e ChromeDriver estão instalados no servidor."
        )


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
    driver = None
    try:
        driver = get_selenium_driver()
        driver.get(url)
        
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cr-standard-grid__item, h1")))
        except:
            time.sleep(1)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        name = "Aluno"
        name_selectors = [
            ('h1', {'class': 'profile-name'}),
            ('h1', {}),
            ('div', {'class': 'cr-profile-header__title'}),
        ]
        
        for tag, attrs in name_selectors:
            name_elem = soup.find(tag, attrs)
            if name_elem:
                name = name_elem.get_text(strip=True)
                break
        
        badge_count = 0
        badge_containers = soup.find_all('div', class_='cr-standard-grid__item')
        if badge_containers:
            badge_count = len(badge_containers)
        
        if badge_count == 0:
            badge_links = soup.find_all('a', href=lambda x: x and '/badges/' in x)
            badge_count = len(badge_links)
        
        if badge_count == 0:
            all_divs = soup.find_all('div')
            for div in all_divs:
                class_str = ' '.join(div.get('class', []))
                if 'badge' in class_str.lower() and 'grid' not in class_str.lower():
                    badge_count += 1
        
        return {
            'name': name,
            'badge_count': badge_count,
            'platform': 'Credly'
        }
    except Exception as e:
        raise Exception(f"Erro ao extrair dados do Credly: {str(e)}")
    finally:
        if driver:
            driver.quit()


def scrape_profile(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    
    if not hostname:
        raise Exception("URL inválida. Por favor, insira um link válido.")
    
    hostname = hostname.lower()
    
    allowed_domains = [
        'credly.com',
        'www.credly.com',
        'skills.google',
        'www.skills.google',
        'cloudskillsboost.google',
        'www.cloudskillsboost.google'
    ]
    
    if hostname not in allowed_domains:
        raise Exception("Plataforma não suportada. Use links do Google Cloud Skills ou Credly.")
    
    if hostname in ['credly.com', 'www.credly.com']:
        return scrape_credly(url)
    elif 'skills.google' in hostname or 'cloudskillsboost.google' in hostname:
        return scrape_google_cloud_skills(url)
    else:
        raise Exception("Plataforma não suportada. Use links do Google Cloud Skills ou Credly.")
