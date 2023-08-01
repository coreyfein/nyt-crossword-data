from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common import exceptions
from datetime import datetime, timedelta
import json


import os

from dotenv import load_dotenv
load_dotenv()

def get_start_and_end_dates():
    start_date_str = str(input('Enter date start (yyyy-mm-dd) > '))
    end_date_str = str(input('Enter date end (yyyy-mm-dd) > '))
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    print(start_date, end_date)
    return start_date, end_date

def open_browser(action):
    print("in open_browser()")
    print(action)
    options = Options()
    options.add_experimental_option("detach", True)
    options.page_load_strategy = 'none'
    # if action == "get_solve_times":
    #     options.add_argument("--headless=new")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver
def login(driver):
    driver.get("https://myaccount.nytimes.com/auth/enter-email")
    # driver.find_element(By.ID, "email").send_keys(NYT_USERNAME)
    # driver.find_element(By.CSS_SELECTOR, 'button[data-testid="submit-email"]').click()
    # WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID, "password"))
    # driver.find_element(By.ID, "password").send_keys(NYT_PASSWORD)
    # WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[data-testid="login-button"]'))
    # driver.find_element(By.CSS_SELECTOR, 'button[data-testid="login-button"]').click()
    WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[data-testid="user-settings-button"]'))#"Account" link on homepage
    cookies = json.dumps(driver.get_cookies())
    print(cookies)
    return cookies

def get_url(date_to_retrieve, start_date):
    year = date_to_retrieve.strftime("%Y")
    month = date_to_retrieve.strftime("%m")
    day = date_to_retrieve.strftime("%d")
    if date_to_retrieve == start_date:
        url = f"https://myaccount.nytimes.com/auth/enter-email?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fcrosswords%2Fgame%2Fdaily%2F{year}%2F{month}%2F{day}&response_type=cookie&client_id=games&application=crosswords&asset=navigation-bar"
    else:
        url = f"https://www.nytimes.com/crosswords/game/daily/{year}/{month}/{day}"

    print(url)
    return url

def get_solve_time(driver, url):
    print(f"getting solve time at url {url}")
    driver.get(url)
    WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]'))
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]').click()
    WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CLASS_NAME, 'timer-count'))
    timer_count = driver.find_element(By.CLASS_NAME, 'timer-count')
    solve_time = timer_count.text
    # WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CLASS_NAME, 'pz-icon pz-icon-pause'))# if that's there, continue to the next day since this one wasn't completed
    
    return solve_time
    

def main():
    start_date, end_date = get_start_and_end_dates()
    date_to_retrieve = start_date
    
    # driver = open_browser("login")
    # cookies = login(driver)
    # driver.quit()

    # driver = open_browser("get_solve_times")
    # for cookie in json.loads(cookies):
    #     try:
    #         driver.add_cookie(cookie)
    #     except exceptions.InvalidCookieDomainException as e:
    #         print(f"InvalidCookieDomainException for this cookie:")
    #         print(cookie)
    driver = open_browser("get_solve_times")
    solve_times_by_date = {}
    while date_to_retrieve <= end_date:
        url = get_url(date_to_retrieve, start_date)
        solve_time = get_solve_time(driver, url)
        date_str = date_to_retrieve.strftime("%Y-%m-%d")
        print(f"{date_str}: {solve_time}")
        solve_times_by_date[date_str] = solve_time
        date_to_retrieve += timedelta(days=1)
        print(solve_times_by_date)
    driver.quit()
    print("quit driver")
    print(solve_times_by_date)
    print("Done.")


def test_eight_components():
    driver = webdriver.Chrome()

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    driver.quit()

if __name__ == "__main__":
    NYT_USERNAME = os.getenv("NYT_USERNAME")
    NYT_PASSWORD = os.getenv("NYT_PASSWORD")
    main()