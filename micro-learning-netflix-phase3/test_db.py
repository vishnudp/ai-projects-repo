# check_db.py

import chromadb

client = chromadb.PersistentClient(
    path="generated/video_db"
)

collection = client.get_collection(
    "course_videos"
)

print("Total Documents:",
      collection.count())

sample = collection.peek(5)

print(sample)