import os
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# replace these with your username and password
USERNAME = os.environ['MONASH_USERNAME']
PASSWORD = os.environ['MONASH_PASSWORD']

data = {
    'th': [],
    'td': []
}


# initialise chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('https://my.monash.edu/wes/exam/results/')


# click login button
try:
    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login-box"]/tbody/tr[2]/td[1]/input[3]'))
    )
    login_btn.click()
except TimeoutException:
    print("Timed out waiting for home page to load")
    sys.exit()
except NoSuchElementException:
    print('An element was missing on browser')
    sys.exit()

# fill login form
try:
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'okta-signin-username'))
    )
    username_input.send_keys(USERNAME)
    
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'okta-signin-password'))
    ) 
    password_input.send_keys(PASSWORD)

    submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'okta-signin-submit'))
    )
    submit_btn.click()
except TimeoutException:
    print("Timed out waiting for login page to load")
    sys.exit()
except NoSuchElementException:
    print('An element was missing on browser')
    sys.exit()


# locate 2-factor authentication button
try:
    auth_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/main/div[2]/div/div/form[1]/div[2]/input'))
    )
    auth_btn.click()
except TimeoutException:
    print("Timed out waiting for 2-factor authentication page to load")
    sys.exit()
except NoSuchElementException:
    print('An element was missing on browser')
    sys.exit()


# press enter after 2-factor authentication
input('Please complete 2-factor authentication and press enter to continue')


# scrape academic record
try:
    for table in driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr/td[2]/div/table[1]'):
        for row in table.find_elements_by_xpath(".//*[self::tr]"):
            for dtype in data:
                content = [cell.text for cell in row.find_elements_by_xpath(f'.//*[self::{dtype}]')]
                if len(content) == 7:
                    data[dtype].append(content)
except NoSuchElementException:
    print('An element was missing on browser')
    sys.exit()


# save as csv
folder_path = os.path.join(os.getcwd(), 'academic_records')
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

df = pd.DataFrame(data['td'], columns=data['th'])
df.to_csv(os.path.join(folder_path, 'latest_record.csv'), index=False)
print(df)