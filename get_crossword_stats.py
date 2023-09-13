from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
import csv
import helpers

def open_browser():
    print("Opening browser")
    options = Options()
    options.add_experimental_option("detach", True)
    options.page_load_strategy = 'none'
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_url(date_to_retrieve, start_date):
    year = date_to_retrieve.strftime("%Y")
    month = date_to_retrieve.strftime("%m")
    day = date_to_retrieve.strftime("%d")
    if date_to_retrieve == start_date:
        url = f"https://myaccount.nytimes.com/auth/enter-email?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fcrosswords%2Fgame%2Fdaily%2F{year}%2F{month}%2F{day}&response_type=cookie&client_id=games&application=crosswords&asset=navigation-bar"
    else:
        url = f"https://www.nytimes.com/crosswords/game/daily/{year}/{month}/{day}"

    return url

def get_solve_time(driver, url):
    print(f"Getting solve time at url: {url}")
    driver.get(url)
    WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]'))
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]').click()
    WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CLASS_NAME, 'timer-count'))
    timer_count = driver.find_element(By.CLASS_NAME, 'timer-count')
    solve_time = timer_count.text
    # WebDriverWait(driver, timeout=1000).until(lambda d: d.find_element(By.CLASS_NAME, 'pz-icon pz-icon-pause'))# if pause icon is there, continue to the next day since this one wasn't completed? 
    # No - instead, just look for solve times under a minute in exported data.
    
    return solve_time

def main():
    start_date, end_date = helpers.get_start_and_end_dates()
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    driver = open_browser()
    
    with open(f'solve_times_{start_date_str}_{end_date_str}.csv', 'w') as f:
        writer = csv.writer(f)
        csv_headers = ['date', 'solve_time']
        writer.writerow(csv_headers)
        solve_times_by_date = {}
        date_to_retrieve = start_date
        while date_to_retrieve <= end_date:
            url = get_url(date_to_retrieve, start_date)
            solve_time = get_solve_time(driver, url)
            date_str = date_to_retrieve.strftime("%Y-%m-%d")
            writer.writerow([date_str, solve_time])
            f.flush()
            print(f"{date_str}: {solve_time}")
            solve_times_by_date[date_str] = solve_time
            date_to_retrieve += timedelta(days=1)
            print(solve_times_by_date)
    driver.quit()
    print(solve_times_by_date)
    print("Done.")

if __name__ == "__main__":
    main()