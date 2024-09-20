from openai import AzureOpenAI

from app.config import settings

openai_client = AzureOpenAI(
    api_key=settings.azure_openai_key,
    azure_endpoint=settings.azure_openai_endpoint,
    api_version="2024-02-15-preview",
)


def generate_answer(question: str, context: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that provides helpful answers based on the provided context. Synthesize the information and respond in your own words. Avoid direct quotes. If the context doesn't contain relevant information, politely say so.",
        },
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {question}\n\nPlease provide an answer based on the context using your own words.",
        },
    ]
    response = openai_client.chat.completions.create(
        model=settings.azure_openai_llm_deployment,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content
