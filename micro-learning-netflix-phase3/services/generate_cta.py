import asyncio
import edge_tts
from pathlib import Path

Path("generated/assets").mkdir(
    parents=True,
    exist_ok=True
)

async def make_cta():

    communicate = edge_tts.Communicate(
        text="Follow for more AI insights",
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save(
        "generated/assets/audio/cta.mp3"
    )

asyncio.run(make_cta())

print("CTA audio generated")