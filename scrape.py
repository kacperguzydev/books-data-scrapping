from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from config import AB_BOOKS_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_links():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(AB_BOOKS_URL)
    driver.implicitly_wait(5)
    links = []

    try:
        filmstrips = driver.find_elements(By.CLASS_NAME, 'product-widget-filmstrip')
        for filmstrip in filmstrips:
            for li in filmstrip.find_elements(By.TAG_NAME, 'li'):
                a_tag = li.find_element(By.TAG_NAME, 'a')
                if a_tag:
                    links.append(a_tag.get_attribute('href'))
    except Exception as e:
        logging.error(f"Error fetching links: {e}")
    finally:
        driver.quit()

    return links


def get_data(links):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    data = []

    try:
        for link in links:
            book_data = {
                'link': None,
                'name': None,
                'price': None
            }
            driver.get(link)
            driver.implicitly_wait(2)
            book_data['link'] = link

            try:
                name = driver.find_element(By.CSS_SELECTOR, '.main-heading')
                book_data['name'] = name.text
            except Exception:
                name = driver.find_element(By.CSS_SELECTOR, '.plp-title')
                book_data['name'] = name.text

            try:
                price = driver.find_element(By.CSS_SELECTOR, '.priceNoBold.x-large')
                book_data['price'] = price.text
            except Exception:
                logging.warning(f"Price not found for link: {link}")

            if book_data['name'] and book_data['price']:
                data.append(book_data)
            else:
                logging.warning(f"Invalid data for link {link}: name or price is missing.")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
    finally:
        driver.quit()

    return data