# SOURCE: https://github.com/sarperavci/CloudflareBypassForScraping





import time
from DrissionPage import ChromiumPage 

class CloudflareBypasser:
    def __init__(self, driver: ChromiumPage):
        self.driver = driver

    def clickCycle(self):
        if self.driver.wait.ele_displayed('#turnstile-wrapper',timeout=1.5):
            self.driver.ele("#turnstile-wrapper", timeout=2.5).click()
 
    def isBypassed(self):
        title = self.driver.title.lower()
        return "just a moment" not in title

    def bypass(self):
        while not self.isBypassed():
            time.sleep(2)
            print("Verification page detected.  Trying to bypass...")
            time.sleep(2)
            self.clickCycle()