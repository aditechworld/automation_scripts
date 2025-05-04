from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time

import pandas as pd

# Reading Excel

df = pd.read_excel("contacts.xlsx")

def get_contact_message_pairs(df, contact_col='phone', message_col='message', send_all_col='send_all'):
    def clean_contact(contact):
        try:
            contact_str = str(contact).strip().replace('.0', '')
            digits = ''.join(filter(str.isdigit, contact_str))
            if len(digits) == 10:
                return int(digits)
        except Exception:
            return None
        return None

    send_all = str(df[send_all_col].iloc[0]).strip().lower() == 'yes' if send_all_col in df.columns else False
    pairs = []
    seen_numbers = set()

    if send_all:
        first_message = df[message_col].dropna().loc[lambda x: x.str.strip() != ''].iloc[0]
        for contact in df[contact_col]:
            cleaned = clean_contact(contact)
            if cleaned is not None and cleaned not in seen_numbers:
                seen_numbers.add(cleaned)
                pairs.append((cleaned, first_message))
    else:
        for _, row in df.iterrows():
            contact = clean_contact(row[contact_col])
            message = str(row[message_col]).strip()
            if contact is not None and contact not in seen_numbers:
                seen_numbers.add(contact)
                pairs.append((contact, message))

    return pairs



# --- Setup Chrome with profile ---
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/session")  # change path
driver = webdriver.Chrome(options=chrome_options)


for number,message in get_contact_message_pairs(df):
    if len(str(message).strip()) == 0:
        continue
    encoded_msg = urllib.parse.quote(message)
    wa_url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}"
    driver.get(wa_url)


    try:
        send_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]')))
        send_btn.click()
        print(f"Message sent to {number}")
    except Exception as e:
        print(f"Failed to send message to {number}")

    time.sleep(3)  # wait between contacts

driver.quit()
