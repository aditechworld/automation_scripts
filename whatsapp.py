from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time

# --- Setup Chrome with profile ---
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/session")  # change path
driver = webdriver.Chrome(options=chrome_options)

# --- List of unsaved contacts ---
numbers = ["918789431995", "917992414822"]  # Add more numbers
message = "Hello! This is a test message from Selenium."
encoded_msg = urllib.parse.quote(message)

for number in numbers:
    wa_url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}"
    driver.get(wa_url)

    try:
        # Click "Continue to Chat"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "action-button"))
        ).click()
    except:
        print(f"No continue button for {number}.")

    try:
        # Click "Use WhatsApp Web"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "use WhatsApp Web"))
        ).click()
    except:
        print(f"No WhatsApp Web button for {number}.")

    try:
        send_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
)
        send_btn.click()
        print(f"Message sent to {number}")
    except Exception as e:
        print(f"Failed to send message to {number}")
        print(f"expection: {e}")

    time.sleep(1)  # wait between contacts

driver.quit()
