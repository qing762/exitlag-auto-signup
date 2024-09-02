import asyncio
import re
import browsers
import warnings
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from DrissionPage import ChromiumPage, ChromiumOptions
from lib.bypass import CloudflareBypasser
from lib.lib import Main
from datetime import datetime

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

async def main():
    lib = Main()
    port = ChromiumOptions().auto_port()

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
        print()

        for i in range(int(executionCount)):
            bar = tqdm(total=100)
            bar.set_description(f"Initial setup completed [{i + 1}/{executionCount}]")
            bar.update(20)
            page = ChromiumPage(port)
            page.listen.start("https://mails.org", method="POST")
            page.get("https://mails.org")
            for _ in range(10):
                result = page.listen.wait()
                if result.url == "https://mails.org/api/email/generate":
                    email = result.response.body["message"]
                    break
            if not email:
                print("Failed to generate email. Exiting...")
                continue
            bar.set_description(f"Generate account process completed [{i + 1}/{executionCount}]")
            bar.update(15)
            tab = page.new_tab("https://www.exitlag.com/register")
            CloudflareBypasser(tab).bypass()
            bar.set_description(f"Bypassed Cloudflare captcha protection [{i + 1}/{executionCount}]")
            bar.update(5)
            print()
            if tab.ele("#inputFirstName", timeout=60):
                tab.ele("#inputFirstName").input("qing")
                tab.ele("#inputLastName").input("chy")
                tab.ele("#inputEmail").input(email)
                tab.ele("#inputNewPassword1").input(passw)
                tab.ele("#inputNewPassword2").input(passw)
                await asyncio.sleep(1)
                page.listen.start("https://mails.org", method="POST")
                tab.ele(".icheck-button").click()
                bar.set_description(f"Signup process completed [{i + 1}/{executionCount}]")
                bar.update(30)
                tab.ele(
                    ".btn btn-primary btn-line fw-500 font-18 py-2 w-100  btn-recaptcha btn-recaptcha-invisible"
                ).click()
                if tab.wait.url_change("https://www.exitlag.com/clientarea.php", timeout=60):
                    if tab.ele(".alert--title", timeout=60):
                        link = None
                        for a in range(10):
                            result = page.listen.wait()
                            content = result.response.body["emails"]
                            if not content:
                                continue 
                            for emailId, y in content.items():
                                if y["subject"] == "[ExitLag] Please confirm your e-mail address":
                                    links = re.findall(
                                        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                        y["body"],
                                    )
                                    for link in links:
                                        if link.startswith("https://www.exitlag.com/user/verify"):
                                            link = re.sub(r"</?[^>]+>", "", link)
                                            break
                                if link:
                                    break
                            if link:
                                break
                        if link:
                            bar.set_description(f"Visiting verify email link [{i + 1}/{executionCount}]")
                            bar.update(20)
                            tab.get(link)
                            await asyncio.sleep(5)
                            bar.set_description(f"Clearing cache and data [{i + 1}/{executionCount}]")
                            bar.update(9)
                            tab.set.cookies.clear()
                            tab.clear_cache()
                            page.set.cookies.clear()
                            page.clear_cache()
                            page.quit()
                            accounts.append({"email": email, "password": passw})
                            bar.set_description(f"All process completed [{i + 1}/{executionCount}]")
                            bar.update(1)
                            bar.close()
                            print()
                        else:
                            print("Failed to find the verify email. Skipping and continuing...\n")
                    else:
                        print("Failed to find the element. Exiting...")
                else:
                    print("Failed to register. Exiting...")
            else:
                print("Failed to load registration page. Exiting...")

        with open("accounts.txt", "a") as f:
            for account in accounts:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(
                    f"Email: {account['email']}, Password: {account['password']}, (Created at {timestamp})\n"
                )
        print("\nAll accounts have been created. Here are the accounts' details:\n")
        for account in accounts:
            print(f"Email: {account['email']}, Password: {account['password']}")
        print("\nThey have been saved to the file accounts.txt.\nHave fun using ExitLag!")

if __name__ == "__main__":
    asyncio.run(main())