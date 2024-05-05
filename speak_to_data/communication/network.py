from collections import namedtuple
import requests

Url = namedtuple("Url", ("base_url", "owner", "model"))

tapas_large = Url("https://api-inference.huggingface.co/models",
                  "google",
                  "tapas-large-finetuned-wtq"
                  )

full_url = "/".join(tapas_large)

API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def call_model_api(payload: str) -> dict:
    response = requests.post(full_url, headers=headers, json=payload)
    return response.json()
