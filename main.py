import requests, httpx, cloudscraper, json, datetime, time, re
from bs4 import BeautifulSoup

client = httpx.Client(http2=True)

url = "https://web2.temp-mail.org/mailbox"
exitlagreg = f"https://www.exitlag.com/api/v2/register"
sitekey = "9ed0f8ae-3e13-4ea8-82eb-2c112b1bc89f"
messageurl = "https://web2.temp-mail.org/messages"

print(
'''
M"""""`'"""`YM                dP             dP                            oo                   d88888P .d8888P d8888b. 
M  mm.  mm.  M                88             88                                                     d8' 88'         `88
M  MMM  MMM  M .d8888b. .d888b88 .d8888b.    88d888b. dP    dP    .d8888b. dP 88d888b. .d8888b.    d8'  88baaa. .aaadP'
M  MMM  MMM  M 88'  `88 88'  `88 88ooood8    88'  `88 88    88    88'  `88 88 88'  `88 88'  `88   d8'   88` `88 88'
M  MMM  MMM  M 88.  .88 88.  .88 88.  ...    88.  .88 88.  .88    88.  .88 88 88    88 88.  .88  d8'    8b. .d8 88.
M  MMM  MMM  M `88888P8 `88888P8 `88888P'    88Y8888' `8888P88    `8888P88 dP dP    dP `8888P88 d8'     `Y888P' Y88888P
MMMMMMMMMMMMMM                                             .88          88                  .88
                                                       d8888P           dP              d8888P
                                                       ''')
time.sleep(3)

key = input(f"\nPlease locate to this URL.\nhttps://hcaptcha.projecttac.com/?sitekey={sitekey}\nComplete the hCaptcha and paste in the h-captcha-response by pressing the copy button.\n")
kk = input(f"\nInput your password for your account. Your password must be at least 6 characters. If you prefer to stay with the default password, ignore this and press enter:")

if kk == "":
  kk = "1234567890"
else:
  kk = kk

scraper = cloudscraper.create_scraper(disableCloudflareV1=True, 
    browser={
        'browser': 'chrome',
        'platform': 'ios',
        'desktop': False,
        'mobile': True
    }
)

reque = scraper.post(url)
if reque.status_code == 200:
  print(f"\nEmail request successfully responded with a status code of {reque.status_code}")
  dat = json.loads(reque.text)
  addr = dat["mailbox"]
  token = dat["token"]
  print(f"Fetching email address success!\n\nToken: {token}\nEmail address: {addr}\n")
else:
  print("Fetch email address fail!\nExiting...")
  exit(reque.status_code)

exitlagpayload = {
  "email": addr,
  "email_confirmation": addr,
  "password": kk,
  "password_confirmation": kk,
  "refer_user": "0",
  "refer_domain": "",
  "recaptchaToken": key,
  "locale": "en"
}

req = requests.post(exitlagreg, data=exitlagpayload)
if req.status_code == 200:
  print(f"\nExitLag request responded with a status code of {req.status_code}")
  data = json.loads(req.text)
  tok = data["token"]
  meid = data["me"]["id"]
  banned = data["me"]["ban"]
  email_approved = data["me"]["email_approved"]
  lan = data["me"]["locale"]
  permission_provider = data["me"]["permission_provider"]

  print(f"ExitLag account registration has completed with the id of {meid}.\n")
  print(f"Token: {tok}\nID: {meid}\nBanned?: {banned}\nEmail approved status: {email_approved}\nLocale: {lan}\nPermission provider: {permission_provider}\n")
else:
  print("ExitLag account registration failed!\nExiting...")
  exit(req.status_code)

header = {
  "authorization": token,
  "cache-control": "no-cache"
}

time.sleep(1)
print("\rPlease wait.", end="")
time.sleep(1)
print("\rPlease wait..", end="")
time.sleep(1)
print("\rPlease wait...", end="")
time.sleep(1)
print("\rPlease wait....", end="")
time.sleep(1)
print("\rPlease wait.....", end="")
time.sleep(1)
print("\rPlease wait....", end="")
time.sleep(1)
print("\rPlease wait....", end="")
time.sleep(1)
print("\rPlease wait...", end="")
time.sleep(1)
print("\rPlease wait..", end="")
time.sleep(1)
print("\rPlease wait.", end="")
time.sleep(1)
print("\rPlease wait..", end="")
time.sleep(1)
print("\rPlease wait...", end="")
time.sleep(1)
print("\rPlease wait....", end="")
time.sleep(1)
print("\rPlease wait.....", end="")
time.sleep(1)
print("\rPlease wait....", end="")
time.sleep(1)
print("\rPlease wait...", end="")
time.sleep(1)
print("\rPlease wait..", end="")
time.sleep(1)
print("\rPlease wait.", end="")
time.sleep(1)
print("\r", end="")

msg = scraper.get(messageurl, headers=header)
if msg.status_code == 200:
  msgtxt = msg.text
  da = json.loads(msgtxt)
  print(f"Fetch email data request responded with a status code of {msg.status_code}\n")
  for x in da["messages"]:
    emailid = x["_id"]
    recievedat = datetime.datetime.fromtimestamp(x["receivedAt"]).strftime('%Y-%m-%d %H:%M:%S')
    fr = x["from"]
    subject = x["subject"]
    bodyPreview = x["bodyPreview"]
    attachmentsCount = x["attachmentsCount"]
  print(f"Email ID: {emailid}\nRecieved at: {recievedat}\nFrom: {fr}\nSubject: {subject}\nBody Preview: {bodyPreview}\nAttachments count: {attachmentsCount}\n")
else:
  print("Fetch email data fail!\nExiting...")
  exit(msg.status_code)

exitlagverifycontent = f"https://web2.temp-mail.org/messages/{emailid}"
ct = scraper.get(exitlagverifycontent, headers=header)
if ct.status_code == 200:
  txt = json.loads(ct.text)
  soup = BeautifulSoup(txt["bodyHtml"], 'html.parser')
  match = re.search(r"https://www.exitlag.com/verify/email/\w+", str(soup))

  if match:
    link = match.group()
    print(f"Please click this URL to verify your email address on ExitLag.\n{link}")
    print(f"\nTo login to ExitLag with your email address created just now, use the following email address: \n{addr}\nand the following password:\n{kk}")
  else:
    print("Link not found!")
else:
  print("Fetch ExitLag verify url failed!\nExiting...")
  exit(ct.status_code)