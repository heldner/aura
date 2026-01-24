from langchain_mistralai import MistralAIEmbeddings


def get_embeddings_model():
    return MistralAIEmbeddings(model="mistral-embed")


def generate_embedding(text: str):
    model = get_embeddings_model()
    return model.embed_query(text)
