from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time

# Phone number in international format (e.g., India)
phone_number = "917992414822"
message = "Hello from Selenium using wa.me!"
encoded_msg = urllib.parse.quote(message)

wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"

# Setup Chrome
driver = webdriver.Chrome()

# Open WhatsApp Web via wa.me link
driver.get(wa_url)

# Click "Continue to Chat" if it appears
try:
    continue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "action-button"))
    )
    continue_btn.click()
except:
    print("No 'Continue to Chat' button found.")

# Click "use WhatsApp Web"
try:
    use_web_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "use WhatsApp Web"))
    )
    use_web_btn.click()
except:
    print("No 'use WhatsApp Web' link found.")

# Wait until user is logged in (wait for h1 "Chats")
print("Waiting for QR scan or WhatsApp Web to load...")
try:
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//h1[text()="Chats"]'))
    )
    print("Logged in!")
except:
    print("Timeout. Login failed.")
    driver.quit()
    exit()

# Wait for message box to appear and send message
try:
    msg_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
    )
    msg_box.send_keys(message)

    send_button = driver.find_element(By.XPATH, '//button[@aria-label="Send"]')
    send_button.click()
    print("Message sent successfully!")

except Exception as e:
    print("Error sending message:", e)

time.sleep(3)
driver.quit()
