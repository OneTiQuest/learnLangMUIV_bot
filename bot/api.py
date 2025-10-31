import requests
import os
from datetime import datetime, timezone
import json


class HttpClient:
    auth = {}  # chat_id: {access_token: str, expires_in: int, refresh_token: str}
    host = f"http://{os.environ.get('HOST_API')}"
    chat_id: str
    headers: dict = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, chat_id: int, bot=None):
        self.chat_id = chat_id
        self.bot = bot

    def log(self, msg):
        msg = json.dumps(msg)
        if self.bot:
            self.bot.send_message(self.chat_id, msg)
        else:
            print(msg)

    def is_login(self):
        return self.chat_id in self.auth

    def set_headers(self):
        auth_data = self.auth and self.auth.get(self.chat_id)
        expires_in = auth_data and auth_data.get("expires_in")

        if expires_in and expires_in < datetime.now(timezone.utc).timestamp():
            return self.refresh_token()

        else:
            self.headers["Authorization"] = f"Bearer {auth_data.get('access_token')}"

    def refresh_token(self):
        auth_data = self.auth.get(self.chat_id)
        refresh_token = auth_data.get("refresh_token")

        self.headers["Authorization"] = f"Bearer {refresh_token}"
        auth_data = requests.post(f"{self.host}/refresh", headers=self.headers).json()

        self.auth[self.chat_id] = {
            "access_token": auth_data.get("access_token"),
            "refresh_token": auth_data.get("refresh_token"),
            "expires_in": auth_data.get("expires_in"),
        }
        self.set_headers()

    def login(self, login: str, password: str, chat_id: int):
        login_data = {"login": login, "password": password, "chat_id": chat_id}
        auth_data = requests.post(
            f"{self.host}/login", json=login_data, headers=self.headers
        ).json()

        if not auth_data or auth_data.get("error"):
            return False

        self.auth[self.chat_id] = {
            "access_token": auth_data.get("access_token"),
            "refresh_token": auth_data.get("refresh_token"),
            "expires_in": auth_data.get("expires_in"),
        }

        self.set_headers()
        return True

    def register(self, data: dict):
        auth_data = requests.post(
            f"{self.host}/register", json=data, headers=self.headers
        ).json()

        if not auth_data or auth_data.get("error"):
            return False

        self.auth[self.chat_id] = {
            "access_token": auth_data.get("access_token"),
            "refresh_token": auth_data.get("refresh_token"),
            "expires_in": auth_data.get("expires_in"),
        }
        self.set_headers()
        return True

    def get(self, url: str):
        self.set_headers()
        return requests.get(self.host + url, headers=self.headers).json()

    def post(self, url: str, data: dict):
        self.set_headers()
        return requests.post(self.host + url, json=data, headers=self.headers).json()

    def put(self, url: str, data: dict):
        self.set_headers()
        return requests.put(self.host + url, json=data, headers=self.headers).json()

    def patch(self, url: str, data: dict):
        self.set_headers()
        return requests.patch(self.host + url, json=data, headers=self.headers).json()

    def delete(self, url: str):
        self.set_headers()
        return requests.delete(self.host + url, headers=self.headers).json()
