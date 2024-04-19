import string
import random
import time
import re
import browsers
import sys
from DrissionPage import ChromiumPage
from requests_html import HTMLSession


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

def wait_until_url(page, target_url, timeout=30):
    """
    Wait until the current URL of the page matches the target URL.

    Parameters:
    page (DrissionPage): The DrissionPage instance.
    target_url (str): The target URL to wait for.
    timeout (int): The maximum time to wait in seconds. Default is 30.

    Returns:
    bool: True if the current URL matches the target URL, False if the timeout is reached.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if page.url == target_url:
            return True
        time.sleep(0.5)
    return False

passw = "Qing762.chy"
maildomain = "mail.gw"

print(
    "\nDue to the inner workings of the module, it is needed to browse programmatically.\nNEVER use the gui to navigate (Using your keybord and mouse) as it will causes POSSIBLE DETECTION!\nThe script will do the entire job itself.\n"
)

request = HTMLSession()
domain = request.get(
    f"https://api.{maildomain}/domains", params={"page": "1"}
).json()
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

page = ChromiumPage()
page.get("https://www.exitlag.com/register")
page.ele('#inputFirstName').input("qing")
page.ele('#inputLastName').input("chy")
page.ele('#inputEmail').input(email)
page.ele('#inputNewPassword1').input(passw)
page.ele('#inputNewPassword2').input(passw)
element = page.ele('.icheck-button')
element.click()
element = page.ele('.btn btn-primary btn-line fw-500 font-18 py-2 w-100  btn-recaptcha btn-recaptcha-invisible')
element.click()
if wait_until_url(page, "https://www.exitlag.com/register-success", timeout=60):
    time.sleep(2)
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
    page.get(f"{link}")
    time.sleep(5)
    page.quit()
    print(f"Your email address: {email}\nYour password: {passw}\n")
    print("Have fun using ExitLag!")
    exit()