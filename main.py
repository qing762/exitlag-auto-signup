import asyncio
import re
import browsers
import aiohttp
import DrissionPage
from DrissionPage import ChromiumPage
from lib.lib import Main
from datetime import datetime


async def main():
    lib = Main()

    await lib.getSettingsAndBlockIP()

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
            async with aiohttp.ClientSession() as session:
                try:
                    if maildomain in ["mail.gw", "mail.tm"]:
                        domain = await lib.getDomain(session, maildomain)
                        for domain_member in domain["hydra:member"]:
                            email, token = await lib.registerAccount(
                                session, maildomain, domain_member, passw
                            )
                    elif maildomain == "ghostlymail.com":
                        async with session.post(
                            "https://www.ghostlymail.com/api/mailboxes"
                        ) as resp:
                            register = await resp.json()
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
                            maildomain = await lib.switchDomain(maildomain, externaldomain)
                            domain = await lib.getDomain(session, maildomain)
                            for domain_member in domain["hydra:member"]:
                                email, token = await lib.registerAccount(
                                    session, maildomain, domain_member, passw
                                )
                        except KeyError:
                            if externaldomain2 == "ghostlymail.com":
                                maildomain = await lib.switchDomain(maildomain, externaldomain2)
                                async with session.post(
                                    "https://www.ghostlymail.com/api/mailboxes"
                                ) as resp:
                                    register = await resp.json()
                                    email = register["emailAddress"]
                                    emailID = register["id"]
                    else:
                        print(
                            "Failed to find selected mail domain.\nThis shouldn't appear in common cases.\nPlease report this in the Discord server (https://qing762.is-a.dev/discord/)\nExiting..."
                        )
                        continue

                page = ChromiumPage()
                page.get("https://www.exitlag.com/register")
                try:
                    page.wait.ele_displayed(page('@src^https://challenges.cloudflare.com/cdn-cgi'))
                    iframe = page('@src^https://challenges.cloudflare.com/cdn-cgi')
                    if iframe:
                        iframe.ele("tag:input").click()
                except DrissionPage.errors.ElementNotFoundError:
                    pass
                if page.ele("#inputFirstName", timeout=60):
                    page.ele("#inputFirstName").input("qing")
                    page.ele("#inputLastName").input("chy")
                    page.ele("#inputEmail").input(email)
                    page.ele("#inputNewPassword1").input(passw)
                    page.ele("#inputNewPassword2").input(passw)
                    await asyncio.sleep(1)
                    page.ele(".icheck-button").click()
                    page.ele(
                        ".btn btn-primary btn-line fw-500 font-18 py-2 w-100  btn-recaptcha btn-recaptcha-invisible"
                    ).click()
                    if page.wait.url_change("https://www.exitlag.com/register-success"):
                        if page.ele(
                            ".h2 text-uppercase fw-600 organetto text-center text-white mb-0",
                            timeout=60,
                        ):
                            if maildomain == "mail.gw" or maildomain == "mail.tm":
                                found = False
                                async with session.get(
                                    f"https://api.{maildomain}/messages",
                                    params={"page": "1"},
                                    headers={"Authorization": f"Bearer {token}"},
                                ) as resp:
                                    msg = await resp.json()
                                    if (
                                        msg["hydra:member"][0]["intro"]
                                        == "Hello and welcome qing! You are now a step away from getting the best communications to improve your gameplay and get rid of…"
                                    ):
                                        msgid = msg["hydra:member"][0]["id"]
                                    else:
                                        msgid = msg["hydra:member"][1]["id"]
                                    async with session.get(
                                        f"https://api.{maildomain}/messages/{msgid}",
                                        params={"id": f"{msgid}"},
                                        headers={"Authorization": f"Bearer {token}"},
                                    ) as resp:
                                        fullmsg = await resp.json()
                                        link = re.findall(
                                            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                            fullmsg["text"],
                                        )[0]
                                        page.get(f"{link}")
                                        await asyncio.sleep(5)
                                        page.set.cookies.clear()
                                        page.clear_cache()
                                        page.quit()
                                        accounts.append({"email": email, "password": passw})
                                        found = True
                                        continue
                            elif maildomain == "ghostlymail.com":
                                async with session.get(
                                    f"https://www.ghostlymail.com/api/mailboxes/{emailID}"
                                ) as resp:
                                    msg = await resp.json()
                                    await asyncio.sleep(1)
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
                                            await asyncio.sleep(5)
                                            page.set.cookies.clear()
                                            page.clear_cache()
                                            page.quit()
                                            accounts.append({"email": email, "password": passw})
                                            found = True
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
                    if not found:
                        print(
                            "Failed to find the verify email. Skipping and continuing...\n"
                        )
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

if __name__ == "__main__":
    asyncio.run(main())
