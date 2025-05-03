from selenium import webdriver;
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


# Load contacts
df = pd.read_excel("contacts.xlsx")
phone_numbers = df['Phone'].dropna().tolist()

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
input("Scan QR code and press Enter here to continue...")

# Click on "New Chat" > "New Group"
time.sleep(10)
new_chat_btn = driver.find_element(By.XPATH, "//div[@title='New chat']")
new_chat_btn.click()

time.sleep(2)
new_group_btn = driver.find_element(By.XPATH, "//div[@title='New group']")
new_group_btn.click()

# Add each contact
for phone in phone_numbers:
    time.sleep(1)
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.clear()
    search_box.send_keys(phone)
    time.sleep(3)
    
    try:
        user = driver.find_element(By.XPATH, f"//span[@title='{phone}']")
        user.click()
    except:
        print(f"Contact {phone} not found or not on WhatsApp.")

# Click Next
time.sleep(2)
next_button = driver.find_element(By.XPATH, "//span[@data-icon='arrow-forward']")
next_button.click()

# Enter group name
time.sleep(2)
group_name = "My Selenium Group"
group_input = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
group_input.send_keys(group_name)

# Finalize group creation
time.sleep(1)
create_button = driver.find_element(By.XPATH, "//span[@data-icon='checkmark']")
create_button.click()

print("Group created successfully!")
