import asyncio
import re
import warnings
import time
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from DrissionPage import Chromium, ChromiumOptions
from lib.bypass import CloudflareBypasser

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


async def main():

    port = ChromiumOptions().auto_port()

    passw = (
        input(
            "\033[1m"
            "\n(RECOMMENDED) Press enter in order to use the default password"
            "\033[0m"
            "\nIf you prefer to use your own password, you need to manually verify its strength at https://www.exitlag.com/register\nPassword: "
        )
        or "Qing762.chy"
    )

    accounts = []
    executionCount = input(
        "\nNumber of accounts to generate (Default: 1): "
    )
    print()
    executionCount = int(executionCount) if executionCount.isdigit() else 1

    for x in range(executionCount):
        bar = tqdm(total=100)
        bar.set_description(f"Initial setup completed [{x + 1}/{executionCount}]")
        bar.update(20)
        chrome = Chromium(addr_or_opts=port)
        page = chrome.get_tab(id_or_num=1)
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

        startTime = time.time()
        while True:
            endTime = time.time()
            if endTime - startTime > 10:
                print("Failed to find captcha. Exiting...")
                return
            else:
                if tab.ele(".:grecaptcha-badge"):
                    break
        tab.ele(".custom-checkbox--input checkbox").click()

        bar.set_description(f"Signup process [{x + 1}/{executionCount}]")
        bar.update(30)

        try:
            tab.ele(
                ".btn btn-primary btn-block  btn-recaptcha btn-recaptcha-invisible"
            ).remove_attr("disabled")
        except Exception:
            pass
        tab.ele(
            ".btn btn-primary btn-block  btn-recaptcha btn-recaptcha-invisible"
        ).click()

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
