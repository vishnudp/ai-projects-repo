import chromadb

client = chromadb.PersistentClient(
    path="generated/video_db"
)

collection = client.get_collection(
    "course_videos"
)

result = collection.get(
    limit=750,
    include=["metadatas"]
)

print(
    result["metadatas"]
)