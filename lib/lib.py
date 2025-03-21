import time
import requests
import sys
import re
from DrissionPage import ChromiumPage


class Main:
    async def checkPassword(self, password):
        hasLowercase = re.search(r'[a-z]', password)
        hasUppercase = re.search(r'[A-Z]', password)
        hasSpecial = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        hasNumber = re.search(r'[0-9]', password)

        if (len(password) >= 8 and
                hasLowercase and
                hasUppercase and
                hasSpecial and
                hasNumber):
            return "\nPassword is valid."
        else:
            if len(password) < 8:
                return "\nPassword does not meet the requirements. Please use at least 8 characters."
            if not hasLowercase:
                return "\nPassword does not meet the requirements. Please use a lowercase letter."
            if not hasUppercase:
                return "\nPassword does not meet the requirements. Please use an uppercase letter."
            if not hasSpecial:
                return "\nPassword does not meet the requirements. Please use at least 1 special character (!@#$%^&*(),.?\":{}|<>)."
            if not hasNumber:
                return "\nPassword does not meet the requirements. Please use at least 1 number."

    async def checkUpdate(self):
        try:
            resp = requests.get(
                "https://api.github.com/repos/qing762/exitlag-auto-signup/releases/latest"
            )
            latestVer = resp.json()["tag_name"]

            if getattr(sys, 'frozen', False):
                import version
                currentVer = version.__version__
            else:
                with open("version.txt", "r") as file:
                    currentVer = file.read().strip()

            if currentVer < latestVer:
                print(f"Update available: {latestVer} (Current version: {currentVer})\nYou can download the latest version from: https://github.com/qing762/exitlag-auto-signup/releases/latest")
            else:
                print(f"You are running the latest version: {currentVer}")
                pass
        except Exception as e:
            print(f"An error occurred: {e}")
            pass

    def testProxy(self, proxy):
        try:
            response = requests.get("http://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
            return True, response.status_code
        except Exception:
            return False, "Proxy test failed! Please ensure that the proxy is working correctly. Skipping proxy usage..."


class CloudflareBypasser:
    # SOURCE: https://github.com/sarperavci/CloudflareBypassForScraping
    def __init__(self, driver: ChromiumPage, max_retries=-1, log=True):
        self.driver = driver
        self.max_retries = max_retries
        self.log = log

    def search_recursively_shadow_root_with_iframe(self, ele):
        try:
            if ele.shadow_root:
                if ele.shadow_root.child().tag == "iframe":
                    return ele.shadow_root.child()
            else:
                for child in ele.children():
                    result = self.search_recursively_shadow_root_with_iframe(child)
                    if result:
                        return result
        except Exception as e:
            self.log_message(f"Error searching shadow root with iframe: {e}")
        return None

    def search_recursively_shadow_root_with_cf_input(self, ele):
        try:
            if ele.shadow_root:
                if ele.shadow_root.ele("tag:input"):
                    return ele.shadow_root.ele("tag:input")
            else:
                for child in ele.children():
                    result = self.search_recursively_shadow_root_with_cf_input(child)
                    if result:
                        return result
        except Exception as e:
            self.log_message(f"Error searching shadow root with CF input: {e}")
        return None

    def locate_cf_button(self):
        try:
            button = None
            eles = self.driver.eles("tag:input")
            for ele in eles:
                if "name" in ele.attrs.keys() and "type" in ele.attrs.keys():
                    if "turnstile" in ele.attrs["name"] and ele.attrs["type"] == "hidden":
                        button = ele.parent().shadow_root.child()("tag:body").shadow_root("tag:input")
                        break

            if button:
                return button
            else:
                self.log_message("Basic search failed. Searching for button recursively.")
                ele = self.driver.ele("tag:body")
                iframe = self.search_recursively_shadow_root_with_iframe(ele)
                if iframe:
                    button = self.search_recursively_shadow_root_with_cf_input(iframe("tag:body"))
                else:
                    self.log_message("Iframe not found. Button search failed.")
                return button
        except Exception as e:
            self.log_message(f"Error locating CF button: {e}")
            return None

    def log_message(self, message):
        if self.log:
            print(message)

    def click_verification_button(self):
        try:
            button = self.locate_cf_button()
            if button:
                self.log_message("Verification button found. Attempting to click.")
                button.click()
            else:
                self.log_message("Verification button not found.")
        except Exception as e:
            self.log_message(f"Error clicking verification button: {e}")

    def is_bypassed(self):
        try:
            title = self.driver.title.lower()
            return "just a moment" not in title
        except Exception as e:
            self.log_message(f"Error checking page title: {e}")
            return False

    def bypass(self):
        try_count = 0

        while not self.is_bypassed():
            if 0 < self.max_retries + 1 <= try_count:
                self.log_message("Exceeded maximum retries. Bypass failed.")
                break

            self.log_message(f"Attempt {try_count + 1}: Verification page detected. Trying to bypass...")
            self.click_verification_button()

            try_count += 1
            time.sleep(2)

        if self.is_bypassed():
            self.log_message("Bypass successful.")
        else:
            self.log_message("Bypass failed.")


if __name__ == "__main__":
    print("This is a library file. Please run main.py instead.")
