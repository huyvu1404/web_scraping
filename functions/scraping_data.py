from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_laptop_data():
    driver = webdriver.Chrome()
    url = f"https://www.thegioididong.com/laptop"
    based_url = "https://www.thegioididong.com"
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    while True:
        try: 
            show_more_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'view-more'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            time.sleep(3) 
            ActionChains(driver).move_to_element(show_more_button).click().perform()
            time.sleep(3)
        except:
            break

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    laptops = []
    for laptop in soup.find_all(class_='item __cate_44'):
        laptop_name_tag = laptop.find("h3")
        laptop_name = laptop_name_tag.get_text(strip=True) if laptop_name_tag else None
        
        laptop_brand_tag = laptop.find('a', class_='main-contain')
        laptop_brand = laptop_brand_tag['data-brand'] if laptop_brand_tag else None
        
        laptop_url_tag = laptop.find('a', class_='main-contain')
        laptop_url = based_url + laptop_url_tag.get('href') if laptop_url_tag else None
        
        laptop_ram_ssd_tag = laptop.find(class_="item-compare gray-bg")
        laptop_ram_ssd = []
        if laptop_ram_ssd_tag:
            for span_tag in laptop_ram_ssd_tag.find_all("span"):
                laptop_ram_ssd.append(span_tag.get_text(strip=True) if span_tag else None)
            laptop_ram = laptop_ram_ssd[0]
            laptop_ssd = laptop_ram_ssd[1]
        else:
            laptop_ram = None
            laptop_ssd = None
        
        laptop_old_price_element = laptop.find(class_='price-old black')    
        laptop_old_price = laptop_old_price_element.get_text(strip=True) if laptop_old_price_element else None
    
        laptop_current_price = laptop.find(class_='price').get_text(strip=True)
    
        laptop_gift_element = laptop.find(class_="item-gift")
        laptop_gift = laptop_gift_element.get_text(strip=True) if laptop_gift_element else None
    
        laptop_rating_element = laptop.find(class_="item-rating-total")
        laptop_rating = laptop_rating_element.get_text(strip=True) if laptop_rating_element else 0
    
        full_stars = len(laptop.find_all('i', class_='icon-star'))
        half_stars = len(laptop.find_all('i', class_='icon-star-half'))
        score = full_stars + 0.5 * half_stars
    
        laptops.append({'name': laptop_name, 'brand': laptop_brand, 'ram': laptop_ram, 'ssd': laptop_ssd, 'old_price': laptop_old_price, 'current_price': laptop_current_price, 'gift': laptop_gift, 'total_rating': laptop_rating, 'avg_score': score, 'link': laptop_url})

    return laptops
    
def scrape_tablet_data():
    driver = webdriver.Chrome()
    url = f"https://www.thegioididong.com/may-tinh-bang"
    based_url = "https://www.thegioididong.com"
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    while True:
        try: 
            show_more_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'view-more'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            time.sleep(3) 
            ActionChains(driver).move_to_element(show_more_button).click().perform()
            time.sleep(3)
        except:
            break

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    tablets = [] 
    for tablet in soup.find_all(class_= 'item ajaxed __cate_522'):
        tablet_name_tag = tablet.find("h3")
        tablet_name = tablet_name_tag.get_text(strip=True) if tablet_name_tag else None
        
        tablet_brand_tag = tablet.find('a', class_='main-contain')
        tablet_brand = tablet_brand_tag['data-brand'] if tablet_brand_tag else None
        
        tablet_url_tag = tablet.find('a', class_='main-contain')
        tablet_url = based_url + tablet_url_tag.get('href') if tablet_url_tag else None
        
        tablet_screen_tag = tablet.find(class_="item-compare gray-bg")
        tablet_screen_details = []
        if tablet_screen_tag:
            for span_tag in tablet_screen_tag.find_all("span"):
                tablet_screen_details.append(span_tag.get_text(strip=True) if span_tag else None)
        tablet_screen = ' '.join(tablet_screen_details)
        
        tablet_old_price_element = tablet.find(class_='price-old black')    
        tablet_old_price = tablet_old_price_element.get_text(strip=True) if tablet_old_price_element else None
    
        tablet_current_price_element = tablet.find(class_='price')
        tablet_current_price = tablet_current_price_element.get_text(strip=True) if tablet_current_price_element else None
        
        tablet_gift_element = tablet.find(class_="item-gift")
        tablet_gift = tablet_gift_element.get_text(strip=True) if tablet_gift_element else None
    
        tablet_rating_element = tablet.find(class_="item-rating-total")
        tablet_rating = tablet_rating_element.get_text(strip=True) if tablet_rating_element else 0
    
        full_stars = len(tablet.find_all('i', class_='icon-star'))
        half_stars = len(tablet.find_all('i', class_='icon-star-half'))
        score = full_stars + 0.5 * half_stars
    
        tablets.append({'name': tablet_name, 'brand': tablet_brand, 'screen': tablet_screen, 'old_price': tablet_old_price, 'current_price': tablet_current_price, 'gift': tablet_gift, 'total_rating': tablet_rating, 'avg_score': score, 'link': tablet_url})
    
    return tablets


def scrape_phone_data():
    driver = webdriver.Chrome()
    url = f"https://www.thegioididong.com/dtdd"
    based_url = "https://www.thegioididong.com"
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    while True:
        try: 
            show_more_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'view-more'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            time.sleep(3) 
            ActionChains(driver).move_to_element(show_more_button).click().perform()
            time.sleep(3)
        except:
            break

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    phones = []
    for phone in soup.find_all(class_= 'item ajaxed __cate_42'):
        phone_name_tag = phone.find("h3")
        phone_name = phone_name_tag.get_text(strip=True) if phone_name_tag else None
        
        phone_brand_tag = phone.find('a', class_='main-contain')
        phone_brand = phone_brand_tag['data-brand'] if phone_brand_tag else None
        
        phone_url_tag = phone.find('a', class_='main-contain')
        phone_url = based_url + phone_url_tag.get('href') if phone_url_tag else None
        
        phone_screen_tag = phone.find(class_="item-compare gray-bg")
        phone_screen_details = []
        if phone_screen_tag:
            for span_tag in phone_screen_tag.find_all("span"):
                phone_screen_details.append(span_tag.get_text(strip=True) if span_tag else None)
        phone_screen = ' '.join(phone_screen_details)
        
        phone_old_price_element = phone.find(class_='price-old black')    
        phone_old_price = phone_old_price_element.get_text(strip=True) if phone_old_price_element else None
    
        phone_current_price_element = phone.find(class_='price')
        phone_current_price = phone_current_price_element.get_text(strip=True) if phone_current_price_element else None
        
        phone_gift_element = phone.find(class_="item-gift")
        phone_gift = phone_gift_element.get_text(strip=True) if phone_gift_element else None
    
        phone_rating_element = phone.find(class_="item-rating-total")
        phone_rating = phone_rating_element.get_text(strip=True) if phone_rating_element else 0
    
        full_stars = len(phone.find_all('i', class_='icon-star'))
        half_stars = len(phone.find_all('i', class_='icon-star-half'))
        score = full_stars + 0.5 * half_stars
    
        phones.append({'name': phone_name, 'brand': phone_brand, 'screen': phone_screen, 'old_price': phone_old_price, 'current_price': phone_current_price, 'gift': phone_gift, 'total_rating': phone_rating, 'avg_score': score, 'link': phone_url})
    
    return phones