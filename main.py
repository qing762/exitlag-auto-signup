import time
import re
import browsers
from DrissionPage import ChromiumPage
from requests_html import HTMLSession
from lib.lib import Main
from datetime import datetime

lib = Main()

lib.getSettingsAndBlockIP()

print("\nEnsuring Chrome availability...")

if browsers.get("chrome") is None:
    print(
        "\nChrome is required for this tool. Please install it via:\nhttps://google.com/chrome"
    )
else:
    passw = input(
        "\nInput your password for your account.\nIt is recommended for you to stay with the default password, ignore this and press enter\nIf you prefer to input your own password, you might need to manually verify the password strength at https://www.exitlag.com/register yourself.\nPassword: "
    )

    if passw == "":
        passw = "Qing762.chy"
    else:
        passw = passw

    accounts = []

    while True:
        maildomain = input(
            "\nChoose your email provider. This can be mail.gw, mail.tm or ghostlymail.com"
            "\nFor mail.gw, type 1 and press enter to continue"
            "\nFor mail.tm, type 2 and press enter to continue."
            "\nFor ghostlymail.com, type 3 and press enter to continue"
            "\nIf nothing is entered, the script will stick to the default provider (ghostlymail.com)"
            "\nOption: "
        )
        if maildomain == "1":
            maildomain = "mail.gw"
            externaldomain = "mail.tm"
            externaldomain2 = "ghostlymail.com"
            break
        elif maildomain == "2":
            maildomain = "mail.tm"
            externaldomain = "mail.gw"
            externaldomain2 = "ghostlymail.com"
            break
        elif maildomain == "3":
            maildomain = "ghostlymail.com"
            externaldomain = "mail.tm"
            externaldomain2 = "mail.gw"
            break
        elif maildomain == "":
            maildomain = "ghostlymail.com"
            externaldomain = "mail.gw"
            externaldomain2 = "mail.tm"
            break
        else:
            print("Invalid number given. Please enter a valid number.")

    while True:
        executionCount = input(
            "\nHow many accounts do you want to create?\nIf nothing is entered, the script will stick to the default value (1)\nAmount: "
        )
        if executionCount == "":
            executionCount = 1
            break
        else:
            try:
                executionCount = int(executionCount)
                break
            except ValueError:
                print("Invalid number given. Please enter a valid number.")

    print(
        "\nDue to the inner workings of the module, it is needed to browse programmatically.\nNEVER use the gui to navigate (Using your keybord and mouse) as it will causes POSSIBLE DETECTION!\nThe script will do the entire job itself.\n"
    )

    for x in range(int(executionCount)):
        request = HTMLSession()
        try:
            if maildomain in ["mail.gw", "mail.tm"]:
                domain = lib.getDomain(request, maildomain)
                for domain_member in domain["hydra:member"]:
                    email, token = lib.registerAccount(
                        request, maildomain, domain_member, passw
                    )
            elif maildomain == "ghostlymail.com":
                register = request.post(
                    "https://www.ghostlymail.com/api/mailboxes"
                ).json()
                email = register["emailAddress"]
                emailID = register["id"]
            else:
                print(
                    "Failed to find selected mail domain.\nThis shouldn't appear in common cases.\nPlease report this in the Discord server (https://qing762.is-a.dev/discord/)\nExiting..."
                )
                continue
        except KeyError:
            if externaldomain in ["mail.gw", "mail.tm"]:
                try:
                    maildomain = lib.switchDomain(maildomain, externaldomain)
                    domain = lib.getDomain(request, maildomain)
                    for domain_member in domain["hydra:member"]:
                        email, token = lib.registerAccount(
                            request, maildomain, domain_member, passw
                        )
                except KeyError:
                    if externaldomain2 == "ghostlymail.com":
                        maildomain = lib.switchDomain(maildomain, externaldomain2)
                        register = request.post(
                            "https://www.ghostlymail.com/api/mailboxes"
                        ).json()
                        email = register["emailAddress"]
                        emailID = register["id"]
            else:
                print(
                    "Failed to find selected mail domain.\nThis shouldn't appear in common cases.\nPlease report this in the Discord server (https://qing762.is-a.dev/discord/)\nExiting..."
                )
                continue

        page = ChromiumPage()
        page.get("https://www.exitlag.com/register")
        if page.ele("#inputFirstName", timeout=60):
            page.ele("#inputFirstName").input("qing")
            page.ele("#inputLastName").input("chy")
            page.ele("#inputEmail").input(email)
            page.ele("#inputNewPassword1").input(passw)
            page.ele("#inputNewPassword2").input(passw)
            element = page.ele(".icheck-button")
            element.click()
            element = page.ele(
                ".btn btn-primary btn-line fw-500 font-18 py-2 w-100  btn-recaptcha btn-recaptcha-invisible"
            )
            element.click()
            if lib.waitUntilUrl(
                page, "https://www.exitlag.com/register-success", timeout=60
            ):
                if page.ele(
                    ".h2 text-uppercase fw-600 organetto text-center text-white mb-0",
                    timeout=60,
                ):
                    if maildomain == "mail.gw" or maildomain == "mail.tm":
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
                        continue
                    elif maildomain == "ghostlymail.com":
                        msg = request.get(
                            f"https://www.ghostlymail.com/api/mailboxes/{emailID}"
                        ).json()
                        found = False
                        for x in msg["emails"]:
                            if (
                                x["subject"]
                                == "[ExitLag] Please confirm your e-mail address"
                            ):
                                link = re.findall(
                                    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                    x["textBody"],
                                )[0]
                                page.get(f"{link}")
                                time.sleep(5)
                                page.quit()
                                accounts.append({"email": email, "password": passw})
                                found = True
                                continue
                        if not found:
                            print(
                                "Failed to find the verify email. Skipping and continuing...\n"
                            )
                            continue
                    else:
                        print(
                            "Failed to selected mail domain.\nThis shouldn't appear in common cases.\nPlease report this in the Discord server (https://qing762.is-a.dev/discord/)\nExiting..."
                        )
                        continue
                else:
                    print("Failed to find the element. Exiting...")
                    continue
            else:
                print("Failed to register. Exiting...")
                continue

    with open("accounts.txt", "a") as f:
        for account in accounts:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"Email: {account['email']}, Password: {account['password']} (Created at {timestamp})\n"
            )
    print("\nAll accounts have been created. Here are the accounts' details:\n")
    for account in accounts:
        print(f"Email: {account['email']}, Password: {account['password']}")
    print("\nThey have been saved to the file accounts.txt.\nHave fun using ExitLag!")
