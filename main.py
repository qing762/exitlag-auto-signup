import string, random, time, re
from selenium.webdriver.support.ui import WebDriverWait
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from seleniumbase import DriverContext
from selenium.webdriver.support import expected_conditions as EC

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

passw = input(f"\nInput your password for your account.\nIt is recommended for you to stay with the default password, ignore this and press enter\nIf you prefer to input your own password, you might need to manually verify the password strength at https://www.exitlag.com/register yourself.\nPassword: ")
if passw == "":
   passw = "Qing762.chy"
else:
   passw = passw

print("\nDue to the inner workings of the module, it is needed to browse programmatically.\nNEVER use the gui to navigate (Using your keybord and mouse) as it will causes POSSIBLE DETECTION!\nThe script will do the entire job itself.\n")

request = HTMLSession()
domain = request.get("https://api.mail.tm/domains", params={"page": "1"}).json()
for x in domain["hydra:member"]:
  register = request.post("https://api.mail.tm/accounts", json={"address": f"{get_random_string(10)}@{x["domain"]}", "password": passw}).json()
  email = register["address"]
token = request.post("https://api.mail.tm/token", json={"address": email, "password": passw}).json()["token"]

with DriverContext(uc=True, headless=False) as browser:
   stealth(browser,
         languages=["en-US", "en"],
         vendor="Google Inc.",
         platform="Win32",
         webgl_vendor="Intel Inc.",
         renderer="Intel Iris OpenGL Engine",
         fix_hairline=True,
   )

   browser.get('http://exitlag.com/register')
   time.sleep(3)
   firstnameelement = browser.find_element(By.NAME, "firstname")
   firstnameelement.send_keys("qing")
   lastnameelement = browser.find_element(By.NAME, "lastname")
   lastnameelement.send_keys("chycr")
   emailelement = browser.find_element(By.NAME, "email")
   emailelement.send_keys(email)
   passwordelement = browser.find_element(By.NAME, "password")
   passwordelement.send_keys(passw)
   password2element = browser.find_element(By.NAME, "password2")
   password2element.send_keys(passw)
   time.sleep(3)
   browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, '//*[@id="frmCheckout"]/p[1]/label/div/ins'))
   time.sleep(0.5)
   browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, '//*[@id="frmCheckout"]/p[2]/input'))
   try:
      element = WebDriverWait(driver=browser, timeout=60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-body"]/div[1]/section/div/div/h2')))
   except:
      print("XPath not found.")
   finally:
      msg = request.get("https://api.mail.tm/messages", params={"page": "1"}, headers={"Authorization": f"Bearer {token}"}).json()
      if msg["hydra:member"][1]["intro"] == "Hello and welcome qing! You are now a step away from getting the best communications to improve your gameplay and get rid of…":
        msgid = msg["hydra:member"][1]["id"]
      else:
        msgid = msg["hydra:member"][0]["id"]
      fullmsg = request.get(f"https://api.mail.tm/messages/{msgid}", params={"id": f"{msgid}"}, headers={"Authorization": f"Bearer {token}"}).json()
      link = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fullmsg["text"])[0]
      browser.get(f"{link}")
      try:
         element = WebDriverWait(driver=browser, timeout=60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-body"]/div[1]/section/div/div/h2')))
      except:
         print("XPath not found.")
      finally:
         browser.quit()
         print(f"Your email address: {email}\nYour password: {passw}\n")
         print("Have fun using ExitLag!\n")
         exit()