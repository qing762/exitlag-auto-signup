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
    start_time = time.time()
    while time.time() - start_time < timeout:
        if page.url == target_url:
            return True
        time.sleep(0.5)
    return False
            
print("\nEnsuring Chrome availability...")

if browsers.get("chrome") is None:
    print(
        "\nChrome is required for this tool. Please install it via:\nhttps://google.com/chrome"
    )
    exit()
else:
    passw = input(
        "\nInput your password for your account.\nIt is recommended for you to stay with the default password, ignore this and press enter\nIf you prefer to input your own password, you might need to manually verify the password strength at https://www.exitlag.com/register yourself.\nPassword: "
    )

    if passw == "":
        passw = "Qing762.chy"
    else:
        passw = passw

    maildomain = input(
        "\nChoose your email provider. This can be either mail.gw or mail.tm\nFor mail.gw, type 1 and press enter to continue while for mail.tm, type 2 and press enter to continue.\nIf nothing is entered, the script will stick to the default provider (mail.tm)\nOption: "
    )
    if maildomain == "1":
        maildomain = "mail.gw"
    elif maildomain == "2":
        maildomain = "mail.tm"
    elif maildomain == "":
        maildomain = "mail.gw"
    else:
        sys.exit("Unknown text given. Exiting...")

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
    time.sleep(5)
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