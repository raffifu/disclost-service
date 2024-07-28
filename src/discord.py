import httpx

class DiscordService():
    def __init__(self, webhook_id: int, webhook_token: str) -> None:
        self.base_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

        self.client = httpx.Client(http2=True)

    def upload(self, filename: str) -> str:
        payload = {"content": open(filename, 'rb')}

        response = self.client.post(self.base_url, files=payload)
        response.raise_for_status()

        response = response.json()
        return response.get("id")

    def delete(self, message_id: str) -> None:
        response = self.client.delete(f"{self.base_url}/messages/{message_id}")
        response.raise_for_status()

    def download_url(self, message_id: int) -> str:
        response = self.client.get(f"{self.base_url}/messages/{message_id}")
        response.raise_for_status()

        response = response.json()
        attachments = response.get("attachments")

        if len(attachments) == 0:
            raise ValueError("Attachment Not Found.")

        return attachments[0].get("url")

    def close(self) -> None:
        self.client.close()
