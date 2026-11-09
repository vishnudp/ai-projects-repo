# services/broll_downloader.py

from pathlib import Path
import requests

BROLL_DIR = Path("generated/broll")
BROLL_DIR.mkdir(parents=True, exist_ok=True)

VIDEOS = {
    "ai": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
    "india": "https://samplelib.com/lib/preview/mp4/sample-10s.mp4",
    "startup": "https://samplelib.com/lib/preview/mp4/sample-15s.mp4",
    "economy": "https://samplelib.com/lib/preview/mp4/sample-20s.mp4",
    "city": "https://samplelib.com/lib/preview/mp4/sample-30s.mp4",
}

def download_brolls():

    for name, url in VIDEOS.items():

        path = BROLL_DIR / f"{name}.mp4"

        if path.exists():
            continue

        print(f"Downloading {name}")

        r = requests.get(url, timeout=30)

        with open(path, "wb") as f:
            f.write(r.content)

    print("B-roll download complete")