import requests

from config import OLLAMA_URL

import time

class OllamaService:

    def generate(
        self,
        prompt,
        model
    ):

        print(f"\nSTARTING MODEL: {model}")

        start = time.time()

        payload = {
            "model": model,
            "prompt": prompt,
            "think": False,
            "stream": False,
            "format": "json",
            "options": {

                "temperature": 0.1,

                "top_p": 0.8,

                "num_predict": 15000
            }
        }

        print(f"\nSTARTING MODEL: {payload}")

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=3000
        )

        

        print(
            f"REQUEST COMPLETED IN "
            f"{time.time() - start:.2f}s"
        )

        result = response.json()["response"]

        print("\n" + "="*100)
        print("MODEL RESPONSE")
        print(result)
        print("="*100 + "\n")

        return result


ollama = OllamaService()