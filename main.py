import asyncio
import re
import browsers
import warnings
import time
from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm
from DrissionPage import ChromiumPage, ChromiumOptions
from lib.bypass import CloudflareBypasser
from lib.lib import Main

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


async def main():
    lib = Main()
    port = ChromiumOptions().auto_port()

    await lib.getSettingsAndBlockIP()

    print("\nEnsuring Chrome availability...")
    if browsers.get("chrome") is None:
        print(
            "\033[1m"
            "\nWarning: A Chrome installation has not been detected! Chrome is required for the use of this tool"
            "\033[0m"
        )
        print(
            "In the case you have an alternate or undetected installation, you may ignore this"
        )

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
        "\033[1m"
        "\n(RECOMMENDED) Press enter in order to generate the default of 1 account"
        "\033[0m"
        "\nNumber of accounts to generate: "
    )
    executionCount = int(executionCount) if executionCount.isdigit() else 1

    print()
    print("\033c\033[3J\033[2J\033[0m\033[H")
    
    for i in range(executionCount):
        bar = tqdm(total=100)
        bar.set_description(f"Initial setup [{i + 1}/{executionCount}]")
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

        bar.set_description(f"Account generation process [{i + 1}/{executionCount}]")
        bar.update(15)

        tab = page.new_tab("https://www.exitlag.com/register")
        CloudflareBypasser(tab).bypass()

        bar.set_description(f"Cloudflare captcha bypass [{i + 1}/{executionCount}]")
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

        bar.set_description(f"Signup process [{i + 1}/{executionCount}]")
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

                for a in range(10):
                    result = page.listen.wait()
                    content = result.response.body["emails"]

                    if not content:
                        continue

                    for emailId, y in content.items():
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
                        f"Verifying email address [{i + 1}/{executionCount}]"
                    )
                    bar.update(20)
                    tab.get(link)

                    bar.set_description(f"Clearing cache and data")
                    bar.update(9)
                    tab.set.cookies.clear()
                    tab.clear_cache()
                    page.set.cookies.clear()
                    page.clear_cache()
                    page.quit()

                    accounts.append({"email": email, "password": passw})

                    bar.set_description(f"Done [{i + 1}/{executionCount}]")
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

    print("\033c\033[3J\033[2J\033[0m\033[H")

    print("\033[1m" "Credentials:")

    for account in accounts:
        print(f"Email: {account['email']}, Password: {account['password']}")
    print("\033[0m" "\nCredentials saved to accounts.txt\nHave fun using ExitLag!")
    input("Press Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
