from pathlib import Path

import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from services.transcript_parser import (
    parse_vtt
)

TRANSCRIPT_DIR = Path(
    "courses/developed_india_2047/transcripts"
)

DB_PATH = "generated/video_db"

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    "course_videos"
)

chunk_id = 0

for transcript_file in TRANSCRIPT_DIR.glob("*.txt"):

    print("Starting indexing...")

    video_name = (
        transcript_file.stem + ".mp4"
    )

    text = transcript_file.read_text(
        encoding="utf-8"
    )

    segments = parse_vtt(text)

    for idx, segment in enumerate(segments):

       

        collection.add(
            documents=[
                str(segment["text"])
            ],
            ids=[
                f"{video_name}_{idx}"
            ],
            metadatas=[{
                "video": str(video_name),
                "start": float(segment["start"]),
                "end": float(segment["end"]),
                "chunk": int(idx)
            }]
        )

        chunk_id += 1

print(
    f"Indexed {chunk_id} chunks"
)

print(
    "Indexed:",
    collection.count(),
    "documents"
)