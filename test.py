from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

# Wait for user to scan QR code
print("Waiting for QR code to be scanned...")
try:
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//h1[text()="Chats"]'))
    )
    print("Logged in successfully!")
    time.sleep(20);
except:
    print("QR code scan timeout. Exiting.")
    driver.quit()
    exit()

# Send message
contact_name = "Jiya"
message = "Hello from Selenium!"

# Search for contact
search_box = driver.find_element(By.XPATH, '//div[@title="Search input textbox"]')
search_box.click()
search_box.send_keys(contact_name)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//span[@title="{contact_name}"]'))
)
contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
contact.click()

msg_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
msg_box.send_keys(message)

send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send"]')
send_button.click()

print("Message sent!")
driver.quit()
