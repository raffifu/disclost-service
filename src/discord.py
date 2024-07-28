import os
from fastapi import UploadFile
import httpx

WEBHOOK_ID = os.getenv("WEBHOOK_ID")
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")


def get_discord():
    discord = DiscordService(WEBHOOK_ID, WEBHOOK_TOKEN)
    try:
        yield discord
    finally:
        discord.close()

class DiscordService:
    def __init__(self, webhook_id: str | None, webhook_token: str | None) -> None:
        if webhook_id == None or webhook_token == None:
            raise ValueError("WEBHOOK_ID and WEBHOOK_TOKEN must be set")

        self.base_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

        self.client = httpx.Client(http2=True)

    def upload(self, file: UploadFile) -> str:
        payload = {"content": (file.filename, file.file.read(), file.content_type)}


        response = self.client.post(self.base_url, files=payload)
        response.raise_for_status()

        response = response.json()
        return response.get("id")

    def delete(self, message_id: str) -> None:
        response = self.client.delete(f"{self.base_url}/messages/{message_id}")
        response.raise_for_status()

    def download_url(self, message_id: str) -> str:
        response = self.client.get(f"{self.base_url}/messages/{message_id}")
        response.raise_for_status()

        response = response.json()
        attachments = response.get("attachments")

        if len(attachments) == 0:
            raise ValueError("Attachment Not Found.")

        return attachments[0].get("url")

    def close(self) -> None:
        self.client.close()
