import chromadb


client = chromadb.PersistentClient(
    path="generated/video_db"
)

collection = client.get_collection(
    "course_videos"
)


def retrieve_best_segment(query):

    result = collection.query(

        query_texts=[query],

        n_results=1

    )

    metadata = result["metadatas"][0][0]

    return {

        "video":
            metadata["video"],

        "start":
            metadata["start"],

        "end":
            metadata["end"]

    }