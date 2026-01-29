from config import settings
from langchain_mistralai import MistralAIEmbeddings


def get_embeddings_model():
    return MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=settings.llm.api_key.get_secret_value(),
    )


def generate_embedding(text: str):
    model = get_embeddings_model()
    return model.embed_query(text)
