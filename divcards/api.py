import requests

from divcards.auth import BearerAuth


class PoEApi:
    def __init__(self):
        self.auth = BearerAuth()
        self.url = "https://api.pathofexile.com"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }

    def get(self, url: str):
        if not url.startswith("/"):
            url = f"/{url}"

        url = url.removesuffix("/")

        return requests.get(f"{self.url}{url}", headers=self.headers, auth=self.auth)

    def stashes(self, league: str):
        res = self.get(f"/stash/{league}")
        stashes = res.json()["stashes"]

        out = []

        for stash in stashes:
            if children := stash.get("children", []):
                for child in children:
                    out.append(child)
            else:
                out.append(stash)

        return out

    def stash(self, league: str, stash_id: str):
        res = self.get(f"/stash/{league}/{stash_id}")

        return res.json()["stash"]
