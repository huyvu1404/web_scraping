from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_basic_info(product_html_class, based_url="https://www.thegioididong.com"):
    """ Trích xuất một số thông tin cơ bản của sản phẩm từ một thẻ HTML.

    Args:
        product_html_class (BeautifulSoup): Đối tượng BeautifulSoup chứa thẻ HTML của sản phẩm.
        based_url (str, optional): URL gốc của trang web. Mặc định là "https://www.thegioididong.com".

    Returns:
        tuple: Bao gồm tên sản phẩm, hãng sản xuất, và URL sản phẩm.
    """
    
    # Lấy tên sản phẩm
    product_name_tag = product_html_class.find("h3")
    product_name = product_name_tag.get_text(strip=True) if product_name_tag else None
    
    # Lấy hãng sản phẩm    
    product_brand_tag = product_html_class.find('a', class_='main-contain')
    product_brand = product_brand_tag['data-brand'] if product_brand_tag else None
    
    # Lấy URL sản phẩm
    product_url_tag = product_html_class.find('a', class_='main-contain')
    product_url = based_url + product_url_tag.get('href') if product_url_tag else None
    
    return product_name, product_brand, product_url

def get_memory_specs(product_html_class):
    """ Trích xuất thông số bộ nhớ của sản phẩm từ một thẻ HTML.

    Args:
        product_html_class (BeautifulSoup): Đối tượng BeautifulSoup chứa thẻ HTML của sản phẩm.

    Returns:
        tuple: Bao gồm thông tin RAM và SSD của sản phẩm.
    """
    
    # Lấy thông tin RAM và SSD của sản phẩm
    laptop_memory_tag = product_html_class.find(class_="item-compare gray-bg")   
    if laptop_memory_tag:
        laptop_ram, laptop_ssd = [span.get_text(strip=True) for span in laptop_memory_tag.find_all("span")] \
                                 if laptop_memory_tag.find_all("span") else (None, None)
        return laptop_ram, laptop_ssd
    
    return None, None

def get_screen_info(product_html_class):
    """ Trích xuất thông số màn hình của sản phẩm từ một thẻ HTML.

    Args:
        product_html_class (BeautifulSoup): Đối tượng BeautifulSoup chứa thẻ HTML của sản phẩm.

    Returns:
        str: Thông tin màn hình của sản phẩm.
    """
    
    # Lấy thông tin RAM và SSD của sản phẩm
    screen_tag = product_html_class.find(class_="item-compare gray-bg")
    
    if screen_tag:
        tablet_screen = ' '.join(span.get_text(strip=True) for span in screen_tag.find_all("span"))
        return tablet_screen
    
    return None

def get_price_and_promotion(product_html_class):
    """ Trích xuất thông tin giá bán và ưu đãi của sản phẩm từ một thẻ HTML.

    Args:
        product_html_class (BeautifulSoup): Đối tượng BeautifulSoup chứa thẻ HTML của sản phẩm.

    Returns:
        tuple: Thông tin giá bán trước đó, giá bán hiện tại và quà tặng kèm theo khi mua sản phẩm.
    """
    
    # Lấy thông tin giá hiện trước đó của sản phẩm
    old_price_tag = product_html_class.find(class_='price-old black')    
    old_price = old_price_tag.get_text(strip=True) if old_price_tag else None

    # Lấy thông tin giá hiện tại của sản phẩm
    current_price_tag = product_html_class.find(class_='price')
    current_price = current_price_tag.get_text(strip=True) if current_price_tag else None
    
    # Lấy thông tin quà tặng đi kèm
    gift_tag = product_html_class.find(class_="item-gift")
    gift = gift_tag.get_text(strip=True) if gift_tag else None

    return old_price, current_price, gift

def get_rating_info(product_html_class):
    """ Trích xuất thông tin đánh giá từ những người đã mua sản phẩm trước đó từ một thẻ HTML.

    Args:
        product_html_class (BeautifulSoup): Đối tượng BeautifulSoup chứa thẻ HTML của sản phẩm.
        
    Returns:
        str: Thông tin tổng số người đánh giá và điểm số đánh giá trung bình của sản phẩm.
    """
    
    # Lấy thông tin tổng số người đánh giá
    rating_tag = product_html_class.find(class_="item-rating-total")
    rating = rating_tag.get_text(strip=True) if rating_tag else 0

    # Lấy thông tin điểm đánh giá của sản phẩm
    full_stars = len(product_html_class.find_all('i', class_='icon-star'))
    half_stars = len(product_html_class.find_all('i', class_='icon-star-half'))
    score = full_stars + 0.5 * half_stars
    
    return rating, score
    
def scrape_data(product_type, product_class, based_url="https://www.thegioididong.com"):
    """ Thu thập thông tin chi tiết về các sản phẩm từ trang web dựa trên loại sản phẩm.

    Args:
        product_type (str): Loại sản phẩm cần lấy dữ liệu 
        based_url (str, optional): URL gốc của trang web. Mặc định là "https://www.thegioididong.com".

    Returns:
        list: Một danh sách các từ điển chứa thông tin đầy đủ của các sản phẩm thu thập được.
    """
    
    if product_type not in ['laptop', 'may-tinh-bang', 'dtdd']:
        raise ValueError("Loại sản phẩm không hợp lệ. Vui lòng chọn một trong các loại: 'laptop', 'tablet', hoặc 'phone'.")
    
    if product_class not in ['item __cate_44', 'item ajaxed __cate_522', 'item ajaxed __cate_42']:
        raise ValueError(("Mã lớp sản phẩm không hợp lệ. Vui lòng chọn theo hướng dẫn sau:\n"
                          "'item __cate_44' dành cho 'laptop',\n"
                          "'item ajaxed __cate_522' dành cho 'may-tinh-bang',\n"
                          "'item ajaxed __cate_42' dành cho 'dtdd'."))
        
    driver = webdriver.Chrome()

    url = f"{based_url}/{product_type}"
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    
    # Sử dụng selenium để lấy hết tất cả các sản phẩm có ở hiện tại
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

    products = []
    
    # Lấy các thông tin của từng sản phầm và lưu chúng dưới dạng một list các dictionary
    for product in soup.find_all(class_=product_class):
        name, brand, url = get_basic_info(product, based_url)
        old_price, current_price, gift = get_price_and_promotion(product)
        total_rating, score = get_rating_info(product) 
        if product_type == 'laptop':
            ram, ssd = get_memory_specs(product)
            
            
            products.append({'name': name, \
                             'brand': brand, \
                             'ram': ram, \
                             'ssd': ssd, \
                             'old_price': old_price, \
                             'current_price': current_price, \
                             'gift': gift, \
                             'total_rating': total_rating, \
                             'avg_score': score, \
                             'link': url})
        else:
            screen = get_screen_info(product)
            products.append({'name': name, \
                             'brand': brand, \
                             'screen': screen, \
                             'old_price': old_price, \
                             'current_price': current_price, \
                             'gift': gift, \
                             'total_rating': total_rating, \
                             'avg_score': score, \
                             'link': url})
    return products
    
