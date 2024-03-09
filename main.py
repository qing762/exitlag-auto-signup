import string
import random
import time
import re
import browsers
import sys
from selenium.webdriver.support.ui import WebDriverWait
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from seleniumbase import DriverContext
from selenium.webdriver.support import expected_conditions as EC


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


maildomain = "mail.tm"
passw = "Qing762.chy"

request = HTMLSession()
domain = request.get(f"https://api.{maildomain}/domains", params={"page": "1"}).json()

for x in domain["hydra:member"]:
    register = request.post(
        f"https://api.{maildomain}/accounts",
        json={
            "address": f'{get_random_string(15)}@{x["domain"]}',
            "password": passw,
        },
    ).json()
    email = register["address"]
token = request.post(
    f"https://api.{maildomain}/token", json={"address": email, "password": passw}
).json()["token"]

print(email)
print(passw)

time.sleep(40)

with DriverContext(uc=True, headless=False, dark_mode=True) as browser:
    msg = request.get(
        f"https://api.{maildomain}/messages",
        params={"page": "1"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    if (
        msg["hydra:member"][0]["intro"]
        == "Hello and welcome qing! You are now a step away from getting the best communications to improve your gameplay and get rid of…"
    ):
        msgid = msg["hydra:member"][0]["id"]
    else:
        msgid = msg["hydra:member"][1]["id"]
    fullmsg = request.get(
        f"https://api.{maildomain}/messages/{msgid}",
        params={"id": f"{msgid}"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    link = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        fullmsg["text"],
    )[0]
    browser.get(f"{link}")
    try:
        element = WebDriverWait(driver=browser, timeout=60).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-body"]/div[1]/section/div/div/h2')
            )
        )
    except Exception:
        print("XPath not found.")
    finally:
        browser.quit()
        print(f"Your email address: {email}\nYour password: {passw}\n")
        print("Have fun using ExitLag!")
        exit()