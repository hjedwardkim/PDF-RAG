from typing import List

from openai import AsyncAzureOpenAI

from app.config import settings

openai_client = AsyncAzureOpenAI(
    api_key=settings.azure_openai_key,
    azure_endpoint=settings.azure_openai_endpoint,
    api_version="2024-02-15-preview",
)


async def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    responses = await openai_client.embeddings.create(
        model=settings.azure_openai_embedding_deployment,
        input=chunks,
    )
    embeddings = [data.embedding for data in responses.data]

    return embeddings


async def generate_query_embedding(query: str) -> List[float]:
    response = await openai_client.embeddings.create(
        model=settings.azure_openai_embedding_deployment,
        input=[query],
    )

    return response.data[0].embedding
