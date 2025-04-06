from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from .models import Comment
from .analysis import analyze_comments_with_openai

def crawl_and_save_comments(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 ... Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://tossinvest.com/")
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.u09klc0")))
    search_button.click()

    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input._1x1gpvi6")))
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = driver.current_url
    stock_code = current_url.split("/")[-1]
    company_name = keyword

    community_tab = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[id*='trigger-community']")
    ))
    community_tab.click()
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    comments = driver.find_elements(By.CSS_SELECTOR, "span[class*='tw-'][class*='1sihfl60']")
    texts = [c.text.replace("더 보기", "").strip() for c in comments if c.text.replace("더 보기", "").strip() != ""]
    texts = list(set(texts))
    for c in texts:
        Comment.objects.create(
            company_name=company_name,
            company_code=stock_code,
            comment=c
        )

    driver.quit()

    if texts:
        analyze_comments_with_openai(texts[:50], company_name)  # 최대 50개 댓글 분석