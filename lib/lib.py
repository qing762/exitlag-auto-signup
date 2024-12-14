import string
import random
import toml
import asyncio
import platform


class Main:
    async def ainput(prompt: str = "") -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, prompt)

    async def getRandomString(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    async def getDomain(self, request, maildomain):
        async with request.get(
            f"https://api.{maildomain}/domains", params={"page": "1"}
        ) as resp:
            return await resp.json()

    async def registerAccount(self, session, maildomain, domain, passw):
        async with session.post(
            f"https://api.{maildomain}/accounts",
            json={
                "address": f'{await self.getRandomString(15)}@{domain["domain"]}',
                "password": passw,
            },
        ) as resp:
            register = await resp.json()
        email = register["address"]
        async with session.post(
            f"https://api.{maildomain}/token",
            json={"address": email, "password": passw},
        ) as resp:
            respJson = await resp.json()
            token = respJson["token"]
        return email, token

    async def switchDomain(maildomain, externaldomain):
        print(
            f"Mail domain {maildomain} is not currently not available. Switching to the domain {externaldomain}..."
        )
        return externaldomain

if __name__ == "__main__":
    print("This is a library file. Please run main.py instead.")
