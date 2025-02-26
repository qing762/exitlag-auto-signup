import asyncio
import re
import warnings
import time
import os
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from DrissionPage import Chromium, ChromiumOptions
from lib.lib import Main, CloudflareBypasser


warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


async def main():
    lib = Main()
    co = ChromiumOptions()
    co.incognito().auto_port().mute(True)

    print("Checking for updates...")
    await lib.checkUpdate()

    while True:
        browserPath = input(
            "\033[1m"
            "\n(RECOMMENDED) Press enter in order to use the default browser path (If you have Chrome installed)"
            "\033[0m"
            "\nIf you prefer to use other Chromium browser other than Chrome, please enter its executable path here. (e.g: C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe)"
            "\nHere are some supported browsers that are tested and able to use:"
            "\n- Chrome"
            "\n- Brave"
            "\nBrowser executable path: "
        ).replace('"', "").replace("'", "")
        if browserPath != "":
            if os.path.exists(browserPath):
                co.set_browser_path(browserPath)
                break
            else:
                print("Please enter a valid path.")
        else:
            break

    while True:
        passw = (
            input(
                "\033[1m"
                "\n(RECOMMENDED) Press enter in order to use the default password"
                "\033[0m"
                "\nIf you prefer to use your own password, do make sure that your password fulfill the below requirements:\n- Use at least 8 characters\n- Use a lowercase letter\n- Use an uppercase letter\n- Use at least 1 special character (!@#$%...)\n- Use at least 1 number\nPassword: "
            )
            or "Qing762.chy"
        )
        if passw != "Qing762.chy":
            result = await lib.checkPassword(passw)
            print(result)
            if "does not meet the requirements" not in result:
                break
        else:
            break

    accounts = []

    while True:
        executionCount = input(
            "\nNumber of accounts to generate (Default: 1): "
        )
        try:
            executionCount = int(executionCount)
            break
        except ValueError:
            if executionCount == "":
                executionCount = 1
                break
            else:
                print("Please enter a valid number.")
    print()

    for x in range(executionCount):
        bar = tqdm(total=100)
        bar.set_description(f"Initial setup completed [{x + 1}/{executionCount}]")
        bar.update(20)
        chrome = Chromium(addr_or_opts=co)
        page = chrome.get_tab(id_or_num=1)
        page.set.window.max()
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

        bar.set_description(f"Account generation process [{x + 1}/{executionCount}]")
        bar.update(15)

        tab = chrome.new_tab("https://www.exitlag.com/register")
        try:
            CloudflareBypasser(tab).bypass()
        except tab.ele("#inputFirstName"):
            pass

        bar.set_description(f"Cloudflare captcha bypass [{x + 1}/{executionCount}]")
        bar.update(5)

        startTime = time.time()
        while True:
            endTime = time.time()
            if endTime - startTime > 10:
                print("Failed to load registration page. Exiting...")
                return
            else:
                if tab.ele("#:fullpage-overlay").style("display") == "none":
                    break

        tab.ele("#inputFirstName").input("qing")
        tab.ele("#inputLastName").input("chy")
        tab.ele("#inputEmail").input(email)
        tab.ele("#inputNewPassword1").input(passw)
        tab.ele("#inputNewPassword2").input(passw)
        page.listen.start("https://mails.org", method="POST")

        tab.ele(".custom-checkbox--input checkbox").click()

        try:
            tab.ele(
                ".btn btn-primary btn-block  btn-recaptcha btn-recaptcha-invisible"
            ).remove_attr("disabled")
        except Exception:
            pass
        tab.ele(
            ".btn btn-primary btn-block  btn-recaptcha btn-recaptcha-invisible"
        ).click()

        bar.set_description(f"Signup process [{x + 1}/{executionCount}]")
        bar.update(30)

        if tab.wait.url_change("https://www.exitlag.com/clientarea.php", timeout=60):
            if tab.ele(".alert--title", timeout=60):
                link = None
                for _ in range(10):
                    result = page.listen.wait()
                    content = result.response.body["emails"]
                    if not content:
                        continue
                    for _, y in content.items():
                        if (
                            y["subject"]
                            == "[ExitLag] Please confirm your e-mail address"
                        ):
                            links = re.findall(
                                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                y["body"],
                            )
                            for link in links:
                                if link.startswith(
                                    "https://www.exitlag.com/user/verify"
                                ):
                                    link = re.sub(r"</?[^>]+>", "", link)
                                    break
                        if link:
                            break
                    if link:
                        break
                if link:
                    bar.set_description(
                        f"Verifying email address [{x + 1}/{executionCount}]"
                    )
                    bar.update(20)
                    tab.get(link)

                    bar.set_description("Clearing cache and data")
                    bar.update(9)
                    tab.set.cookies.clear()
                    tab.clear_cache()
                    chrome.set.cookies.clear()
                    chrome.clear_cache()
                    chrome.quit()

                    accounts.append({"email": email, "password": passw})

                    bar.set_description(f"Done [{x + 1}/{executionCount}]")
                    bar.update(1)
                    bar.close()
                    print()
                else:
                    print(
                        "Failed to find verification email. You may need to verify it manually. Skipping and continuing...\n"
                    )
        else:
            print("Failed to register. Exiting...")

    with open("accounts.txt", "a") as f:
        for account in accounts:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(
                f"Email: {account['email']}, Password: {account['password']}, (Created at {timestamp})\n"
            )

    print("\033[1m" "Credentials:")

    for account in accounts:
        print(f"Email: {account['email']}, Password: {account['password']}")
    print("\033[0m" "\nCredentials saved to accounts.txt\nHave fun using ExitLag!")

if __name__ == "__main__":
    asyncio.run(main())
