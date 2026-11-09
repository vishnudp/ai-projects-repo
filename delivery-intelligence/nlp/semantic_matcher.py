from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.intent_library import INTENTS


class SemanticMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.examples = []
        self.labels = []

        for intent, phrases in INTENTS.items():

            for phrase in phrases:

                self.examples.append(phrase)
                self.labels.append(intent)

        self.embeddings = self.model.encode(
            self.examples
        )

    def classify(self, question):

        query_embedding = self.model.encode(
            [question]
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        best_idx = similarities.argmax()

        return {
            "intent": self.labels[best_idx],
            "score": float(similarities[best_idx])
        }