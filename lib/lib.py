import string
import random
import time
import toml
import platform


class Main():
    def getRandomString(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def waitUntilUrl(self, page, targetUrl, timeout=30):
        startTime = time.time()
        while time.time() - startTime < timeout:
            if page.url == targetUrl:
                return True
            time.sleep(0.5)
        return False

    def getDomain(self, request, maildomain):
        return request.get(f"https://api.{maildomain}/domains", params={"page": "1"}).json()

    def registerAccount(self, request, maildomain, domain, passw):
        register = request.post(
            f"https://api.{maildomain}/accounts",
            json={
                "address": f'{self.getRandomString(15)}@{domain["domain"]}',
                "password": passw,
            },
        ).json()
        email = register["address"]
        token = request.post(
            f"https://api.{maildomain}/token", json={"address": email, "password": passw}
        ).json()["token"]
        return email, token

    def switchDomain(maildomain, externaldomain):
        print(f"Mail domain {maildomain} is not currently not available. Switching to the domain {externaldomain}...")
        return externaldomain

    def getSettingsAndBlockIP(self):
        try:
            data = toml.load("settings.toml")
        except FileNotFoundError:
            data = {
                "blockIP": {
                    "blocked": False
                }
            }

        if "allowed" not in data["blockIP"]:
            while True:
                selection = input("Due to a known issue of 0 trial days cause by the IP address *.exitlag.net, do you want to block the IP address? (y/n): ")
                if str(selection).capitalize() == "Y":
                    data["blockIP"]["allowed"] = True
                    break
                elif str(selection).capitalize() == "N":
                    data["blockIP"]["allowed"] = False
                    break
                else:
                    print("Invalid input. Please try again.")

        if data["blockIP"].get("allowed", False) and not data["blockIP"].get("blocked", False):
            target = ["104.22.79.205", "104.22.78.205", "172.67.29.58"]
            system = platform.system()
            if system == "Windows":
                hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
            else:
                hostsPath = "/etc/hosts"
            try:
                with open(hostsPath, "a") as hostsFile:
                    for x in target:
                        hostsFile.write(f"\n127.0.0.1    {x}\n")
                        print(f"Blocked {x} in the host file.")
                data["blockIP"]["blocked"] = True
                print("Be sure to use a HWID spoofer as well to get the 3 days trial. One of the suggested spoofer is Monotone HWID Spoofer (https://github.com/sr2echa/Monotone-HWID-Spoofer).")
            except PermissionError:
                print("Permission denied. Please run the program as an administrator. This should be done once only!")
                exit(-1)

        with open("settings.toml", "w") as f:
            toml.dump(data, f)


if __name__ == "__main__":
    print("This is a library file. Please run main.py instead.")
